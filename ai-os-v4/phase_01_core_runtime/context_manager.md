---
title: Context Manager & Window Optimization Specification
document_id: SPEC-P01-KERN-006
phase: phase_01_core_runtime
version: 1.0.0
status: APPROVED
owner: Memory & Context Working Group
last_updated: 2026-08-05
---

# Context Manager & Window Optimization Specification

## Executive Summary
This document specifies the Context Manager (`context_manager`), which manages token window allocation, dynamic prompt compression, sliding-window truncation, key information extraction, and context hydration across LLM provider calls in AI OS v4.

---

## 1. Context Compression & Hydration Pipeline

```text
[ RAW AGENT MEMORY & PROMPT TEMPLATE ]
                  │
                  ▼
+-------------------------------------------------------------+
| 1. TOKEN COUNT CALCULATION & WINDOW BOUNDARY CHECK          |
+-------------------------------------------------------------+
                  │ (If Token Count > Provider Ceiling, e.g. 128k)
                  ▼
+-------------------------------------------------------------+
| 2. CONTEXT COMPRESSION & SUMMARIZATION ENGINE               |
|    - Preserve System Prompt & Required Schemas              |
|    - Compress Working History via Recurrent Summarizer      |
+-------------------------------------------------------------+
                  │
                  ▼
+-------------------------------------------------------------+
| 3. HYDRATED PROMPT PAYLOAD (Ready for LLM Ingestion)        |
+-------------------------------------------------------------+
```

---

## 2. Context Manager API Contract

```typescript
export interface ContextWindowConfig {
  readonly maxTokens: number;
  readonly reservedForCompletion: number;
  readonly compressionStrategy: "SLIDING_WINDOW" | "SEMANTIC_SUMMARY" | "HYBRID";
}

export interface HydratedContext {
  readonly systemPrompt: string;
  readonly formattedMessages: Array<{ role: "system" | "user" | "assistant"; content: string }>;
  readonly tokenCount: number;
  readonly compressionRatio: number;
}

export interface IContextManager {
  hydrateContext(taskId: string, config: ContextWindowConfig): Promise<HydratedContext>;
  compressContext(messages: Array<{ role: string; content: string }>, targetTokens: number): Promise<Array<{ role: string; content: string }>>;
  getTokenCount(text: string, model: string): number;
}
```

---

## 3. Compression Rules & Invariants

1. **System Prompt Protection**: System prompt and active schema definitions MUST NEVER be truncated or compressed.
2. **Deterministic Token Calculation**: Uses model-specific tokenizers (e.g. `tiktoken` for OpenAI, `cl100k_base`) to guarantee zero token overflow exceptions (`ERR-AGENT-CONTEXT-OVERFLOW`).

---

## 4. Verification Protocol

```bash
agy verify-context-manager --test-compression --target-tokens 4000
```
Runs context hydration benchmark, verifies compression ratio metrics, and ensures zero schema truncation.
