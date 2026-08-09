"""
AI OS Master Registry Service — exposes system capability lifecycle statuses and discovery APIs.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

REGISTRY_DIR = Path(__file__).parent.parent.resolve() / "registry"

class MasterRegistry:
    @staticmethod
    def get_status() -> Dict[str, Any]:
        result = {}
        for yaml_file in REGISTRY_DIR.glob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
                key = yaml_file.stem
                result[key] = data
            except Exception:
                pass
        return result

    @staticmethod
    def find_agent_by_id(agent_id: str) -> Optional[dict]:
        status = MasterRegistry.get_status()
        agents = status.get("agents", {}).get("agents", [])
        for agent in agents:
            if agent.get("id") == agent_id:
                return agent
        return None

    @staticmethod
    def find_workflow_by_id(workflow_id: str) -> Optional[dict]:
        status = MasterRegistry.get_status()
        workflows = status.get("workflows", {}).get("workflows", [])
        for wf in workflows:
            if isinstance(wf, dict) and wf.get("id") == workflow_id:
                return wf
        return None

    @staticmethod
    def print_summary() -> str:
        status = MasterRegistry.get_status()
        output = ["AI OS CAPABILITY STATUS\n"]
        for category, items in status.items():
            output.append(f"{category.capitalize()}")
            if isinstance(items, dict):
                for subk, sublist in items.items():
                    if isinstance(sublist, list):
                        output.append(f"  {subk.capitalize()}: {len(sublist)}")
            elif isinstance(items, list):
                output.append(f"  Total: {len(items)}")
        return "\n".join(output)

if __name__ == "__main__":
    print(MasterRegistry.print_summary())
