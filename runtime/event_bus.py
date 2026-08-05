"""
AI OS Event Bus — pub/sub message broker for inter-agent communication.

Architecture:
- Topic-based publish/subscribe pattern
- All events follow the event_payload_schema.json contract
- Subscribers receive events matching their registered topics
- Event persistence determined by event_topics.yaml (persistence_required field)
- Full audit trail for all critical events
"""

import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass, field, asdict


logger = logging.getLogger("ai_os.event_bus")


@dataclass
class Event:
    """Standard AI OS event payload per event_payload_schema.json"""
    event_type: str
    agent_id: str
    task_id: str
    payload: dict
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    workflow_id: Optional[str] = None
    severity: str = "info"
    state: Optional[str] = None
    artifacts: List[dict] = field(default_factory=list)
    budget: Optional[dict] = None
    quality: Optional[dict] = None
    next_actions: List[str] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class EventBus:
    """
    AI OS Event Bus — in-process pub/sub broker.

    For production deployments, replace with:
    - Redis Streams (low-latency, durable)
    - Apache Kafka (high-throughput, partitioned)
    - Google Pub/Sub (cloud-native, scalable)

    This implementation provides the full interface contract
    that all agents program against.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._event_history: List[dict] = []
        self._persistence_topics: set = set()
        logger.info("EventBus initialized")

    def configure_persistence(self, persistent_topics: List[str]) -> None:
        """Mark topics as requiring persistence per event_topics.yaml."""
        self._persistence_topics.update(persistent_topics)
        logger.info(f"Persistence configured for {len(persistent_topics)} topics")

    def subscribe(self, topic: str, handler: Callable[[Event], None]) -> None:
        """Register a handler for events on the specified topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        logger.debug(f"Subscriber registered for topic: {topic}")

    def unsubscribe(self, topic: str, handler: Callable) -> None:
        """Remove a handler from a topic."""
        if topic in self._subscribers:
            self._subscribers[topic] = [
                h for h in self._subscribers[topic] if h != handler
            ]

    def publish(self, event: Event) -> int:
        """
        Publish an event to all registered subscribers.

        Returns the number of subscribers notified.
        Persists event if topic is marked as persistence_required.
        """
        if not isinstance(event, Event):
            raise ValueError("Published object must be an Event instance")

        # Validate required fields
        if not event.event_type or not event.agent_id or not event.task_id:
            raise ValueError(
                "Event must have event_type, agent_id, and task_id"
            )

        # Persist if required
        if event.event_type in self._persistence_topics:
            self._event_history.append(event.to_dict())

        # Log all events
        logger.info(
            f"[{event.event_type}] agent={event.agent_id} "
            f"task={event.task_id} trace={event.trace_id} "
            f"severity={event.severity}"
        )

        # Dispatch to subscribers
        handlers = self._subscribers.get(event.event_type, [])
        notified = 0
        for handler in handlers:
            try:
                handler(event)
                notified += 1
            except Exception as e:
                logger.error(
                    f"Handler error for topic {event.event_type}: {e}",
                    exc_info=True
                )

        return notified

    def get_history(
        self,
        topic: Optional[str] = None,
        task_id: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> List[dict]:
        """Retrieve persisted event history with optional filters."""
        history = self._event_history
        if topic:
            history = [e for e in history if e["event_type"] == topic]
        if task_id:
            history = [e for e in history if e["task_id"] == task_id]
        if trace_id:
            history = [e for e in history if e["trace_id"] == trace_id]
        return history

    def subscriber_count(self, topic: str) -> int:
        return len(self._subscribers.get(topic, []))


# Global singleton event bus instance
_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """Get or create the global EventBus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus
