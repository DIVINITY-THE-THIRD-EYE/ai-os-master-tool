import os
import json
import sys

schema_dir = r"c:\Users\PC\OneDrive\Documents\Master tool\ai-os-v4\phase_11_schemas"

required_files = [
    "agent_schema.json",
    "workflow_schema.json",
    "task_schema.json",
    "decision_schema.json",
    "artifact_schema.json",
    "prompt_schema.json",
    "memory_schema.json",
    "knowledge_schema.json",
    "event_schema.json",
    "message_schema.json",
    "project_schema.json",
    "verification_schema.json",
    "policy_schema.json",
    "plugin_schema.json",
    "capability_schema.json",
    "session_schema.json",
    "context_schema.json",
    "kernel_config_schema.json",
    "scheduler_config_schema.json",
    "resource_schema.json",
    "audit_log_schema.json",
    "telemetry_schema.json",
    "error_schema.json",
    "user_schema.json",
    "organization_schema.json",
    "role_schema.json",
    "permission_schema.json",
    "sandbox_config_schema.json",
    "metric_schema.json",
    "template_schema.json",
    "skill_manifest_schema.json",
    "execution_trace_schema.json",
    "model_config_schema.json",
    "eval_result_schema.json",
    "quality_gate_schema.json",
    "rate_limit_schema.json",
    "escalation_schema.json",
    "reflection_schema.json",
    "tradeoff_schema.json",
    "cost_report_schema.json"
]

if not os.path.exists(schema_dir):
    print(f"ERROR: Directory {schema_dir} does not exist.")
    sys.exit(1)

files_in_dir = os.listdir(schema_dir)
json_files = [f for f in files_in_dir if f.endswith(".json")]

print(f"Found {len(json_files)} .json files in {schema_dir}.")
if len(json_files) < 40:
    print(f"ERROR: Expected at least 40 JSON schema files, but found {len(json_files)}.")
    sys.exit(1)

missing_files = []
for req in required_files:
    if req not in files_in_dir:
        missing_files.append(req)

if missing_files:
    print(f"ERROR: The following required schema files are missing: {missing_files}")
    sys.exit(1)

required_keys = ["$schema", "title", "type", "properties"]
failed_files = []

for file_name in json_files:
    file_path = os.path.join(schema_dir, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        missing_keys = [k for k in required_keys if k not in data]
        if missing_keys:
            print(f"ERROR: File {file_name} missing required schema fields: {missing_keys}")
            failed_files.append(file_name)
        elif not isinstance(data.get("properties"), dict):
            print(f"ERROR: File {file_name} field 'properties' is not an object/dict.")
            failed_files.append(file_name)
    except Exception as e:
        print(f"ERROR: File {file_name} failed JSON parsing: {e}")
        failed_files.append(file_name)

if failed_files:
    print(f"FAILED verification for {len(failed_files)} files.")
    sys.exit(1)
else:
    print("SUCCESS: All 40 JSON schema files exist, are valid JSON, and contain $schema, title, type, and properties!")
