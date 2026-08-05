# Experience Repository Specification

> **Subsystem:** Phase 05 — Knowledge Platform  
> **Document ID:** SPEC-05-ER-007  
> **Status:** Approved / Production Grade  
> **Target Release:** AI OS v4.0  

---

## 1. System Overview & Episodic Knowledge Capture

The Experience Repository records, indexes, analyzes, and redistributes multi-agent task execution trajectories. By capturing step-by-step agent decisions, tool invocations, mistakes, self-corrections, and final outcomes, the system provides episodic memory for high-level pattern mining and automated context injection.

---

## 2. Episodic Experience Data Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "EpisodicExperienceRecord",
  "type": "object",
  "properties": {
    "experience_id": { "type": "string", "pattern": "^exp_[a-f0-9]{12}$" },
    "task_id": { "type": "string" },
    "domain": { "type": "string" },
    "agent_role": { "type": "string" },
    "initial_goal": { "type": "string" },
    "outcome_status": { "type": "string", "enum": ["SUCCESS", "FAILURE", "PARTIAL_RECOVERY"] },
    "quality_score": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "execution_time_ms": { "type": "integer" },
    "token_consumption": {
      "type": "object",
      "properties": {
        "prompt_tokens": { "type": "integer" },
        "completion_tokens": { "type": "integer" },
        "total_cost_usd": { "type": "number" }
      }
    },
    "action_trajectory": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "step_number": { "type": "integer" },
          "thought_reasoning": { "type": "string" },
          "tool_call": { "type": "string" },
          "tool_input": { "type": "object" },
          "tool_output_summary": { "type": "string" },
          "self_correction_applied": { "type": "boolean" }
        },
        "required": ["step_number", "tool_call"]
      }
    },
    "key_lessons_extracted": {
      "type": "array",
      "items": { "type": "string" }
    }
  },
  "required": ["experience_id", "task_id", "domain", "agent_role", "initial_goal", "outcome_status", "quality_score", "action_trajectory"]
}
```

---

## 3. Indexing & Similarity Retrieval Pipeline

1. **Context Vectorization:** Goal statement and initial task context are embedded using `text-embedding-3-large`.
2. **Dense Vector Search:** High-confidence historical trajectories matching the current agent goal are retrieved via Qdrant/Milvus.
3. **Trajectory Filtering:** Filters out experiences with `quality_score < 0.85` unless querying specifically for failure post-mortems.

---

## 4. PII Sanitization & Security Filter

Before any experience record is committed to the shared repository:
- **Regex Scrubbing:** Social security numbers, API keys, private certificates, and JWT tokens are sanitized with `[REDACTED_SECRET]`.
- **DLP Presidio Engine:** PII (names, emails, IP addresses) replaced with synthetic domain identifiers.
- **Payload Hash Signature:** SHA-256 hash appended to guarantee sanitized payload immutability.

---

## 5. Integration Contracts with Agent Framework

```python
# Reference implementation for Experience Ingestion
class ExperienceRepositoryManager:
    def commit_trajectory(self, raw_trace: TaskExecutionTrace) -> str:
        sanitized_trace = self.dlp_sanitizer.scrub(raw_trace)
        quality_score = self.evaluation_engine.evaluate(sanitized_trace)
        
        record = EpisodicExperienceRecord(
            experience_id=f"exp_{uuid4().hex[:12]}",
            task_id=raw_trace.task_id,
            domain=raw_trace.domain,
            agent_role=raw_trace.agent_role,
            initial_goal=raw_trace.goal,
            outcome_status=raw_trace.status,
            quality_score=quality_score,
            action_trajectory=sanitized_trace.steps
        )
        
        self.vector_store.insert(record.to_vector_point())
        self.doc_store.save(record)
        return record.experience_id
```

---

## 6. Performance Metrics & Storage Budget

- **Query Latency:** Nearest 5 experience trajectories retrieved P95 < 85 ms.
- **Repository Retention Policy:** Successful trajectories retained indefinitely; uninformative runs pruned after 90 days.
- **Storage Footprint:** Compression ratio 4.2:1 using ZSTD compression on historic trajectory JSONs.
