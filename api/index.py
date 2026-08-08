"""
Vercel Serverless Function Entry Point for AI OS Master Tool REST API.
Mounts the FastAPI runtime app for serverless deployment on Vercel.
"""

import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add skill path to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ai-os-v4", "ai-os-multi-agent-skill"))

from runtime.agent_registry import AgentRecord, AgentRegistry
from runtime.api_server import create_app
from runtime.bootstrap import bootstrap_persistence
from runtime.event_bus import EventBus
from runtime.llm_router import LLMRouter
from runtime.memory_manager import MemoryManager

# Initialize core services
agent_registry = AgentRegistry()
event_bus = EventBus()
llm_router = LLMRouter()

# Persistence Subsystem Wiring
if os.getenv("VERCEL") == "1":
    default_db = "/tmp/local_os_state.db"
else:
    default_db = os.path.join(os.path.dirname(__file__), "..", "local_os_state.db")
db_path = os.getenv("DB_PATH", default_db)
is_supabase = bool(os.getenv("SUPABASE_DATABASE_URL") or os.getenv("DATABASE_URL"))
enable_vram_image = True

state_manager = bootstrap_persistence(db_path, is_supabase, enable_vram_image, event_bus)
memory_manager = MemoryManager(state_manager=state_manager)

# Register standard A01-A13 agents
AGENTS_DEF = [
    ("A01", "Intake Requirements Agent", "1.0.0", ["task_intake", "requirements_analysis"]),
    ("A02", "Context Memory Agent", "1.0.0", ["context_retrieval", "working_memory"]),
    ("A03", "Knowledge Graph Agent", "1.0.0", ["knowledge_graph", "ontology_mapping"]),
    ("A04", "Scheduler Agent", "1.0.0", ["dag_scheduling", "workflow_planning"]),
    ("A05", "Domain Authority Agent", "1.0.0", ["architecture_design", "domain_governance"]),
    ("A06", "Worker Agent", "1.0.0", ["code_generation", "task_execution"]),
    ("A07", "Verification Agent", "1.0.0", ["quality_assurance", "verification"]),
    ("A08", "Policy Decision Agent", "1.0.0", ["policy_evaluation", "compliance_check"]),
    ("A09", "Security Compliance Agent", "1.0.0", ["security_audit", "vulnerability_scan"]),
    ("A10", "Release Deployment Agent", "1.0.0", ["release_management", "deployment"]),
    ("A11", "Observability Operations Agent", "1.0.0", ["monitoring", "telemetry"]),
    ("A12", "Learning Agent", "1.0.0", ["reflection", "learning_opt"]),
    ("A13", "Human Collaboration Agent", "1.0.0", ["human_escalation", "approval_gates"]),
]

for aid, name, ver, caps in AGENTS_DEF:
    rec = AgentRecord(agent_id=aid, name=name, version=ver, capabilities=caps, skills=[], tools=[], permissions=[])
    try:
        agent_registry.register(rec)
        agent_registry.configure(aid)
        agent_registry.mark_ready(aid)
    except Exception as e:
        logger.error(f"Failed to register agent {aid}: {e}", exc_info=True)

app = create_app(
    agent_registry=agent_registry,
    event_bus=event_bus,
    llm_router=llm_router,
    state_manager=state_manager,
)
