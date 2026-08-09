"""
AIOS Tool Gateway — Isolated sandbox execution gatekeeper.
Enforces the mandatory rule: No agent may call a tool directly.
All tool calls pass through CapabilityBroker authorization before sandboxed execution.
"""

from typing import Dict, Any, Callable, Optional
from pydantic import BaseModel, Field
from security.contracts import ToolCallRequest, CapabilityBrokerResult
from execution.capability_broker import CapabilityBroker


class ToolExecutionResult(BaseModel):
    success: bool
    output: Any
    error: Optional[str] = None
    broker_result: CapabilityBrokerResult


class ToolGateway:
    def __init__(self, capability_broker: CapabilityBroker):
        self.capability_broker = capability_broker
        self.sandbox_tools: Dict[str, Callable[..., Any]] = {}

    def register_tool(self, tool_name: str, tool_func: Callable[..., Any]) -> None:
        self.sandbox_tools[tool_name] = tool_func

    def invoke_tool(self, request: ToolCallRequest) -> ToolExecutionResult:
        # 1. Mandatory Capability & Policy Broker Check
        broker_result = self.capability_broker.authorize_tool_call(request)
        if not broker_result.allowed:
            return ToolExecutionResult(
                success=False,
                output=None,
                error=f"CapabilityBroker Enforcement: {broker_result.reason}",
                broker_result=broker_result
            )

        # 2. Retrieve Sandboxed Tool
        tool_func = self.sandbox_tools.get(request.tool_name)
        if not tool_func:
            return ToolExecutionResult(
                success=False,
                output=None,
                error=f"Sandbox Error: Tool '{request.tool_name}' is not registered in sandbox gateway.",
                broker_result=broker_result
            )

        # 3. Execute in Isolated Catch-Block Sandbox
        try:
            output = tool_func(**request.parameters)
            return ToolExecutionResult(
                success=True,
                output=output,
                error=None,
                broker_result=broker_result
            )
        except Exception as e:
            return ToolExecutionResult(
                success=False,
                output=None,
                error=f"Tool Runtime Exception: {str(e)}",
                broker_result=broker_result
            )
