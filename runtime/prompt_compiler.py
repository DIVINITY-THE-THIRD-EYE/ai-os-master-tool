"""
AI OS Prompt Compiler — dynamic prompt compilation engine for task-specific execution contexts.

Compiles:
Base Agent + Task + Domain + Policies + Security + Tools + Memory + Quality Gates + Platform Instructions = Compiled Execution Context
"""

from typing import Dict, List, Optional, Any

VERSION = "1.0.0"

class PromptCompiler:
    VERSION = VERSION

    @staticmethod
    def compile_prompt(
        base_prompt: str,
        task_description: str,
        domain_rules: Optional[List[str]] = None,
        security_policy: Optional[str] = None,
        tools: Optional[List[str]] = None,
        memory_context: Optional[str] = None,
        quality_gates: Optional[Dict[str, Any]] = None,
        platform_instructions: Optional[str] = None,
    ) -> str:
        compiled_parts = [
            f"=== COMPILER VERSION: {PromptCompiler.VERSION} ===",
            f"=== BASE ROLE & PROMPT ===\n{base_prompt.strip()}",
            f"=== TASK OBJECTIVE ===\n{task_description.strip()}"
        ]
        
        if domain_rules:
            compiled_parts.append("=== DOMAIN CONSTRAINTS ===\n" + "\n".join(f"- {r}" for r in domain_rules))
            
        if security_policy:
            compiled_parts.append(f"=== SECURITY POLICY ===\n{security_policy.strip()}")
            
        if tools:
            compiled_parts.append("=== AVAILABLE TOOLS ===\n" + ", ".join(tools))
            
        if memory_context:
            compiled_parts.append(f"=== RELEVANT MEMORY CONTEXT ===\n{memory_context.strip()}")
            
        if quality_gates:
            compiled_parts.append(f"=== REQUIRED QUALITY GATES ===\n{quality_gates}")

        if platform_instructions:
            compiled_parts.append(f"=== PLATFORM INSTRUCTIONS ===\n{platform_instructions.strip()}")
            
        return "\n\n".join(compiled_parts)
