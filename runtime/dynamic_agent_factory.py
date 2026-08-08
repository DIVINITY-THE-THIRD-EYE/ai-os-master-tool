import uuid
from typing import Dict, Any, Optional
import yaml
from pathlib import Path

class DynamicAgentFactory:
    """
    Factory for instantiating dynamic specialist agents and micro-workers 
    on demand from templates, addressing the gap between the 13 canonical 
    agents and the 35+ planned dynamic capabilities.
    """
    def __init__(self, templates_dir: str = "agents/templates"):
        self.templates_dir = Path(templates_dir)
        self.active_dynamic_agents: Dict[str, Any] = {}
        
    def _load_template(self, template_name: str) -> dict:
        """Loads a YAML or Markdown frontmatter template."""
        template_path = self.templates_dir / f"{template_name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Dynamic template {template_name} not found at {template_path}")
        
        # Simplified parser for the purpose of the factory
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        return yaml.safe_load(parts[1])
                    except yaml.YAMLError:
                        pass
        return {}

    def spawn_agent(self, role_type: str, domain_context: dict, budget: int = 100) -> dict:
        """
        Spawns a new dynamic agent for a specific task.
        Assigns an ephemeral ID (e.g. D-1234).
        """
        template_data = self._load_template("dynamic_agent_template")
        
        agent_id = f"D-{str(uuid.uuid4())[:8].upper()}"
        
        agent_instance = {
            "agent_id": agent_id,
            "role": role_type,
            "base_capabilities": template_data.get("capabilities", []),
            "context": domain_context,
            "budget": budget,
            "status": "active"
        }
        
        self.active_dynamic_agents[agent_id] = agent_instance
        return agent_instance
        
    def terminate_agent(self, agent_id: str) -> bool:
        """Cleans up an ephemeral dynamic agent."""
        if agent_id in self.active_dynamic_agents:
            self.active_dynamic_agents[agent_id]["status"] = "terminated"
            del self.active_dynamic_agents[agent_id]
            return True
        return False
