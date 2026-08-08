"""
AI OS Memory Manager — multi-tier memory system managing Working Memory,
Session Memory, Persistent Memory, and Knowledge Graph interface.

Per skill.yaml:
- working_memory: enabled
- session_memory: enabled
- persistent_memory: governed
- knowledge_graph: enabled
- experience_repository: enabled
"""

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ai_os.memory_manager")


@dataclass
class KnowledgeNode:
    node_id: str
    label: str
    node_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeEdge:
    source_id: str
    target_id: str
    relation: str
    weight: float = 1.0


class MemoryManager:
    """
    Multi-tier memory manager for AI OS runtime.
    """

    def __init__(self, state_manager: Any = None):
        self.state_manager = state_manager
        self._working_memory: Dict[str, Dict[str, Any]] = {}
        self._session_memory: Dict[str, List[Dict[str, Any]]] = {}
        self._persistent_memory: Dict[str, Dict[str, Any]] = {}
        self._knowledge_nodes: Dict[str, KnowledgeNode] = {}
        self._knowledge_edges: List[KnowledgeEdge] = []
        self._experience_repository: List[Dict[str, Any]] = []

        if self.state_manager:
            try:
                for key, entry in self.state_manager.list_persistent_memory().items():
                    self._persistent_memory[key] = entry
            except Exception as e:
                logger.error(f"Failed to load persistent memory from state manager: {e}")

    # ---------------------------------------------------------------------------
    # Working Memory (Task Scope)
    # ---------------------------------------------------------------------------

    def set_working_memory(self, task_id: str, key: str, value: Any) -> None:
        """Store key-value in task working memory."""
        if task_id not in self._working_memory:
            self._working_memory[task_id] = {}
        self._working_memory[task_id][key] = value

    def get_working_memory(self, task_id: str, key: Optional[str] = None) -> Any:
        """Retrieve task working memory key or all keys."""
        task_mem = self._working_memory.get(task_id, {})
        if key is None:
            return dict(task_mem)
        return task_mem.get(key)

    def clear_working_memory(self, task_id: str) -> None:
        """Clear task working memory upon completion."""
        self._working_memory.pop(task_id, None)

    # ---------------------------------------------------------------------------
    # Session Memory (Workflow Trace Scope)
    # ---------------------------------------------------------------------------

    def append_session_event(self, session_id: str, event: Dict[str, Any]) -> None:
        """Record an event in the session timeline."""
        if session_id not in self._session_memory:
            self._session_memory[session_id] = []
        event_entry = dict(event)
        event_entry["timestamp"] = time.time()
        self._session_memory[session_id].append(event_entry)

    def get_session_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get ordered session event history."""
        return list(self._session_memory.get(session_id, []))

    # ---------------------------------------------------------------------------
    # Persistent Memory (Governed Store)
    # ---------------------------------------------------------------------------

    def save_persistent(self, key: str, value: Any, tags: Optional[List[str]] = None) -> None:
        """Save a item to governed persistent memory."""
        tags = tags or []
        self._persistent_memory[key] = {
            "value": value,
            "tags": tags,
            "updated_at": time.time(),
        }
        if self.state_manager:
            self.state_manager.save_persistent_memory(key, value, tags)

    def get_persistent(self, key: str) -> Optional[Any]:
        """Get value from persistent memory."""
        entry = self._persistent_memory.get(key)
        return entry["value"] if entry else None

    def search_persistent_by_tag(self, tag: str) -> Dict[str, Any]:
        """Search persistent memory entries by tag."""
        results = {}
        for key, entry in self._persistent_memory.items():
            if tag in entry.get("tags", []):
                results[key] = entry["value"]
        return results

    # ---------------------------------------------------------------------------
    # Knowledge Graph Operations
    # ---------------------------------------------------------------------------

    def add_node(self, node_id: str, label: str, node_type: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Add node to knowledge graph."""
        attributes = attributes or {}
        self._knowledge_nodes[node_id] = KnowledgeNode(
            node_id=node_id,
            label=label,
            node_type=node_type,
            attributes=attributes,
        )
        if self.state_manager:
            self.state_manager.save_knowledge_node(node_id, label, node_type, attributes)

    def add_edge(self, source_id: str, target_id: str, relation: str, weight: float = 1.0) -> None:
        """Add edge to knowledge graph."""
        edge = KnowledgeEdge(source_id=source_id, target_id=target_id, relation=relation, weight=weight)
        self._knowledge_edges.append(edge)
        if self.state_manager:
            self.state_manager.save_knowledge_edge(source_id, target_id, relation, weight)

    def get_related_nodes(self, node_id: str, relation: Optional[str] = None) -> List[KnowledgeNode]:
        """Find nodes connected to a given node."""
        if self.state_manager:
            nodes_data = self.state_manager.get_related_nodes(node_id, relation)
            return [KnowledgeNode(**nd) for nd in nodes_data]

        target_ids = []
        for edge in self._knowledge_edges:
            if edge.source_id == node_id and (relation is None or edge.relation == relation):
                target_ids.append(edge.target_id)
        return [self._knowledge_nodes[tid] for tid in target_ids if tid in self._knowledge_nodes]

    # ---------------------------------------------------------------------------
    # Experience Repository (Lessons Learned)
    # ---------------------------------------------------------------------------

    def record_experience(
        self, task_type: str, outcome: str, lesson: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Record an experience entry for agent reflection."""
        metadata = metadata or {}
        exp = {
            "task_type": task_type,
            "outcome": outcome,
            "lesson": lesson,
            "metadata": metadata,
            "recorded_at": time.time(),
        }
        self._experience_repository.append(exp)
        if self.state_manager:
            self.state_manager.save_experience(task_type, outcome, lesson, metadata)

    def get_experiences(self, task_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get past experience logs filtered by task type."""
        if self.state_manager:
            return self.state_manager.get_experiences(task_type)

        if not task_type:
            return list(self._experience_repository)
        return [e for e in self._experience_repository if e["task_type"] == task_type]

    # ---------------------------------------------------------------------------
    # Context Compression Utility
    # ---------------------------------------------------------------------------

    def compress_context(self, context: Dict[str, Any], max_chars: int = 4000) -> str:
        """
        Compress context dict into a prompt-friendly string within token budget limits.
        """
        raw_json = json.dumps(context, indent=2)
        if len(raw_json) <= max_chars:
            return raw_json

        # Truncate large lists/nested values gracefully
        summary = {}
        for k, v in context.items():
            if isinstance(v, list):
                summary[k] = f"[List of {len(v)} items]"
            elif isinstance(v, dict):
                summary[k] = f"[Dict with keys: {list(v.keys())}]"
            elif isinstance(v, str) and len(v) > 200:
                summary[k] = v[:200] + "... [truncated]"
            else:
                summary[k] = v

        return json.dumps(summary, indent=2)
