"""
AI OS FastAPI REST Server — HTTP API gateway for task submission, agent
discovery, event dispatching, and system monitoring.

Per requirements.txt & platform configuration:
- POST /v1/tasks
- GET  /v1/tasks/{task_id}
- GET  /v1/agents
- POST /v1/events
- GET  /v1/health
- GET  /v1/usage
"""

import logging
import uuid
from typing import Any, Dict, Optional

logger = logging.getLogger("ai_os.api_server")

# Try loading FastAPI; provide stdlib fallback if not installed
FASTAPI_AVAILABLE = False
try:
    from fastapi import Body, FastAPI, HTTPException
    from pydantic import BaseModel, Field

    FASTAPI_AVAILABLE = True
except ImportError:
    logger.info("FastAPI/Pydantic not installed; API server available via standard library runner")


# ---------------------------------------------------------------------------
# Data Transfer Objects
# ---------------------------------------------------------------------------

if FASTAPI_AVAILABLE:

    class TaskSubmissionRequest(BaseModel):
        objective: str = Field(..., description="Task objective/requirements text")
        agent_id: Optional[str] = Field("A01", description="Target initial agent ID")
        workflow_id: Optional[str] = Field(None, description="Optional custom workflow ID")
        metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

    class EventPublishRequest(BaseModel):
        event_type: str = Field(..., description="Topic name e.g. task.created")
        agent_id: str = Field(..., description="Publishing agent ID")
        task_id: str = Field(..., description="Associated task ID")
        payload: Dict[str, Any] = Field(default_factory=dict)


def create_app(
    agent_registry=None,
    event_bus=None,
    workflow_executor=None,
    llm_router=None,
    state_manager=None,
) -> Any:
    """Factory creating configured FastAPI app or fallback runner."""

    if not FASTAPI_AVAILABLE:
        # Return lightweight API router wrapper for non-FastAPI environments
        class FallbackAPIRouter:
            def __init__(self):
                self.agent_registry = agent_registry
                self.event_bus = event_bus
                self.workflow_executor = workflow_executor
                self.llm_router = llm_router
                self.state_manager = state_manager
                self.tasks: Dict[str, Dict[str, Any]] = {}

            def health_check(self) -> Dict[str, Any]:
                return {"status": "healthy", "mode": "production", "fastapi_installed": False}

            def submit_task(self, payload: Dict[str, Any]) -> Dict[str, Any]:
                task_id = f"task-{uuid.uuid4().hex[:8]}"
                record = {
                    "task_id": task_id,
                    "objective": payload.get("objective", ""),
                    "status": "received",
                    "result": None,
                }
                self.tasks[task_id] = record
                return record

            def get_task(self, task_id: str) -> Dict[str, Any]:
                if task_id not in self.tasks:
                    return {"error": f"Task '{task_id}' not found"}
                return self.tasks[task_id]

            def list_agents(self) -> Dict[str, Any]:
                if self.agent_registry:
                    return {
                        "agents": [a.__dict__ if hasattr(a, "__dict__") else a for a in self.agent_registry.list_all()]
                    }
                return {"agents": []}

        return FallbackAPIRouter()

    app = FastAPI(
        title="AI OS v4 Core REST API",
        description="Production API Gateway for Multi-Agent AI OS Orchestration Platform",
        version="1.0.0",
    )

    tasks_store: Dict[str, Dict[str, Any]] = {}

    @app.get("/v1/health")
    def health_check():
        return {
            "status": "healthy",
            "version": "1.0.0",
            "fastapi_installed": True,
            "agent_registry_connected": agent_registry is not None,
            "event_bus_connected": event_bus is not None,
        }

    @app.post("/v1/tasks")
    def submit_task(request: TaskSubmissionRequest):
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task_record = {
            "task_id": task_id,
            "objective": request.objective,
            "initial_agent": request.agent_id,
            "status": "accepted",
            "result": None,
            "metadata": request.metadata,
        }
        tasks_store[task_id] = task_record

        if event_bus:
            from runtime.event_bus import Event

            event_bus.publish(
                Event(
                    event_type="task.created",
                    agent_id=request.agent_id or "A01",
                    task_id=task_id,
                    payload={"objective": request.objective},
                )
            )

        return task_record

    @app.get("/v1/tasks/{task_id}")
    def get_task(task_id: str):
        if task_id not in tasks_store:
            raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")
        return tasks_store[task_id]

    @app.get("/v1/agents")
    def list_agents():
        if agent_registry:
            records = agent_registry.list_all()
            return {"agents": [r.__dict__ if hasattr(r, "__dict__") else r for r in records]}
        return {"agents": []}

    @app.post("/v1/events")
    def publish_event(request: EventPublishRequest):
        if not event_bus:
            raise HTTPException(status_code=503, detail="EventBus service unavailable")
        from runtime.event_bus import Event

        event = Event(
            event_type=request.event_type,
            agent_id=request.agent_id,
            task_id=request.task_id,
            payload=request.payload,
        )
        subscribers_notified = event_bus.publish(event)
        return {"event_id": event.event_id, "subscribers_notified": subscribers_notified}

    @app.get("/v1/usage")
    def get_usage():
        if llm_router:
            return llm_router.get_total_usage()
        return {"total_calls": 0, "total_tokens": 0, "total_cost_usd": 0.0}

    return app
