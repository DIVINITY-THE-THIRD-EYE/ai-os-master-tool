# AI OS v4 — OpenAPI & gRPC API Reference

**Document Version:** 4.0.0  
**Phase:** Phase 15 — Enterprise Documentation  
**Classification:** Enterprise Kernel Interface Reference  
**Status:** Frozen / Production Standard  

---

## 1. Core Platform REST API Specification (OpenAPI 3.0)

Base Endpoint: `https://api.aios.enterprise.internal/v4`

```yaml
openapi: 3.0.3
info:
  title: AI OS v4 Core Kernel REST API
  version: 4.0.0
  description: Official REST API for task orchestration, agent lifecycle, memory querying, and tool execution.

paths:
  /v4/tasks:
    post:
      summary: Create & Submit Orchestration Task
      operationId: createTask
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateTaskRequest'
      responses:
        '201':
          description: Task created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'

  /v4/tasks/{taskId}:
    get:
      summary: Retrieve Task Status & Artifacts
      operationId: getTask
      parameters:
        - name: taskId
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Task details retrieved
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'

  /v4/tools/invoke:
    post:
      summary: Execute Tool via Sandbox Router
      operationId: invokeTool
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ToolInvocationRequest'
      responses:
        '200':
          description: Tool executed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ToolInvocationResponse'

components:
  schemas:
    CreateTaskRequest:
      type: object
      required: [tenant_id, goal_description, workflow_id]
      properties:
        tenant_id: { type: string }
        goal_description: { type: string }
        workflow_id: { type: string }
        input_parameters: { type: object }
        priority: { type: integer, default: 1 }

    TaskResponse:
      type: object
      required: [task_id, status, tenant_id]
      properties:
        task_id: { type: string }
        status: { type: string, enum: [SCHEDULING, EXECUTING, UNDER_REVIEW, COMPLETED, FAILED] }
        tenant_id: { type: string }
        created_at: { type: string, format: date-time }
        artifacts_generated: { type: array, items: { type: string } }

    ToolInvocationRequest:
      type: object
      required: [tool_id, agent_id, parameters]
      properties:
        tool_id: { type: string }
        agent_id: { type: string }
        parameters: { type: object }

    ToolInvocationResponse:
      type: object
      required: [execution_id, status, result]
      properties:
        execution_id: { type: string }
        status: { type: string, enum: [SUCCESS, ACCESS_DENIED, FAILED] }
        result: { type: object }
        execution_time_ms: { type: integer }
```

---

## 2. Core Kernel gRPC Protobuf Contract

```protobuf
syntax = "proto3";

package aios.kernel.v4;

option go_package = "github.com/enterprise/ai-os-v4/pkg/api/v4";

service AgentRuntimeKernelService {
  rpc SubmitTask (SubmitTaskRequest) returns (SubmitTaskResponse);
  rpc StreamTaskStatus (TaskStatusStreamRequest) returns (stream TaskStatusUpdate);
  rpc QueryMemory (MemoryQueryRequest) returns (MemoryQueryResponse);
  rpc CommitCandidateMemory (CandidateMemoryCommitRequest) returns (CommitResponse);
}

message SubmitTaskRequest {
  string tenant_id = 1;
  string agent_id = 2;
  string workflow_id = 3;
  bytes input_json = 4;
  int32 priority_level = 5;
}

message SubmitTaskResponse {
  string task_id = 1;
  string status = 2;
  int64 timestamp_ms = 3;
}

message TaskStatusStreamRequest {
  string task_id = 1;
}

message TaskStatusUpdate {
  string task_id = 1;
  string state = 2;
  string progress_message = 3;
  int32 percent_complete = 4;
}

message MemoryQueryRequest {
  string tenant_id = 1;
  string query_vector = 2;
  int32 max_results = 3;
}

message MemoryQueryResponse {
  repeated MemoryItem items = 1;
}

message MemoryItem {
  string memory_id = 1;
  string content = 2;
  float similarity_score = 3;
}

message CandidateMemoryCommitRequest {
  string candidate_id = 1;
  string proof_id = 2;
}

message CommitResponse {
  bool success = 1;
  string transaction_id = 2;
}
```

---

## 3. Summary Checklist for API Reference Compliance

- [x] OpenAPI 3.0 REST endpoints (`/v4/tasks`, `/v4/tools/invoke`) documented.
- [x] Complete REST JSON request/response schema components included.
- [x] Protobuf gRPC service contract (`AgentRuntimeKernelService`) defined.
