# AI OS v4 — Multi-Language SDK Documentation

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Enterprise SDK Integration Reference  
**Status:** Frozen / Production Standard  

---

## 1. Overview & SDK Architecture

AI OS v4 provides production SDKs for **TypeScript**, **Python**, and **Go**. The SDKs abstract task submission, tool registration, agent definition, event streaming, and memory querying.

---

## 2. TypeScript SDK Specification (`@aios/sdk`)

### 2.1 Installation

```bash
npm install @aios/sdk
```

### 2.2 Usage Example

```typescript
import { AIOSClient, TaskPriority } from "@aios/sdk";

const client = new AIOSClient({
  endpoint: "https://api.aios.enterprise.internal/v4",
  apiKey: process.env.AIOS_API_KEY!,
  tenantId: "tenant_enterprise_alpha"
});

async function main() {
  const task = await client.tasks.create({
    workflowId: "wf.engineering.software_development",
    goalDescription: "Implement JWT auth middleware in Go",
    priority: TaskPriority.HIGH,
    inputParameters: {
      repo_url: "https://github.com/enterprise/backend-service.git"
    }
  });

  console.log(`Task submitted with ID: ${task.taskId}`);

  // Stream task status updates
  client.tasks.streamStatus(task.taskId, (update) => {
    console.log(`[${update.state}] ${update.percentComplete}% - ${update.progressMessage}`);
  });
}

main().catch(console.error);
```

---

## 3. Python SDK Specification (`aios-sdk`)

### 3.1 Installation

```bash
pip install aios-sdk
```

### 3.2 Usage Example

```python
import os
from aios_sdk import AIOSClient, TaskPriority

client = AIOSClient(
    endpoint="https://api.aios.enterprise.internal/v4",
    api_key=os.getenv("AIOS_API_KEY"),
    tenant_id="tenant_enterprise_alpha"
)

def run():
    task = client.tasks.create(
        workflow_id="wf.research.literature_review",
        goal_description="Extract state-of-the-art LLM alignment papers",
        priority=TaskPriority.NORMAL,
        input_parameters={"query": "Direct Preference Optimization 2025"}
    )
    print(f"Task created: {task.task_id}")
    
    result = task.wait_for_completion(timeout_seconds=300)
    print(f"Task completed with artifacts: {result.artifacts}")

if __name__ == "__main__":
    run()
```

---

## 4. Go SDK Specification (`github.com/enterprise/ai-os-v4/pkg/sdk`)

### 4.1 Usage Example

```go
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/enterprise/ai-os-v4/pkg/sdk"
)

func main() {
	client, err := sdk.NewClient(sdk.Config{
		Endpoint: "https://api.aios.enterprise.internal/v4",
		APIKey:   "secret_key_v4",
		TenantID: "tenant_enterprise_alpha",
	})
	if err != nil {
		log.Fatalf("Failed to initialize client: %v", err)
	}

	task, err := client.SubmitTask(context.Background(), sdk.TaskRequest{
		WorkflowID:      "wf.security.audit",
		GoalDescription: "Audit dependencies in main branch",
		Priority:        sdk.PriorityHigh,
	})
	if err != nil {
		log.Fatalf("Failed to submit task: %v", err)
	}

	fmt.Printf("Successfully created task: %s\n", task.TaskID)
}
```

---

## 5. Summary Checklist for SDK Documentation Compliance

- [x] Multi-language support (TypeScript, Python, Go) documented.
- [x] Client initialization, task creation, streaming, and execution code samples provided.
- [x] Canonical package names and installation procedures locked.
