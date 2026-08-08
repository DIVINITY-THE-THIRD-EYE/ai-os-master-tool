"""
AI OS Master Registry Service — exposes system capability lifecycle statuses.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

REGISTRY_DIR = Path(r"c:\Users\PC\OneDrive\Documents\Master tool\registry")

class MasterRegistry:
    @staticmethod
    def get_status() -> Dict[str, Any]:
        result = {}
        for yaml_file in REGISTRY_DIR.glob("*.yaml"):
            try:
                data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
                key = yaml_file.stem
                if isinstance(data, dict):
                    result[key] = data
                else:
                    result[key] = data
            except Exception:
                pass
        return result

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
