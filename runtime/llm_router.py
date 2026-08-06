"""
AI OS Multi-Provider LLM Router — AI Gateway for model selection, dispatch,
failover, token tracking, and structured response parsing.

Supports:
- Gemini (Google Generative AI)
- OpenAI (GPT-4o / GPT-4o-mini / GPT-3.5)
- Anthropic (Claude 3.5 Sonnet / Claude 3 Opus)
- Mock fallback mode when API keys are not present (for offline/test execution)
"""

import json
import logging
import os
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger("ai_os.llm_router")


class ProviderType(Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"


@dataclass
class ModelConfig:
    provider: ProviderType
    model_name: str
    temperature: float = 0.2
    max_tokens: int = 4096
    cost_per_1k_input: float = 0.0015
    cost_per_1k_output: float = 0.002


DEFAULT_MODEL_ROUTING = {
    "A01": ModelConfig(ProviderType.GEMINI, "gemini-1.5-pro", temperature=0.1),
    "A02": ModelConfig(ProviderType.GEMINI, "gemini-2.0-flash", temperature=0.1),
    "A03": ModelConfig(ProviderType.GEMINI, "gemini-1.5-pro", temperature=0.2),
    "A04": ModelConfig(ProviderType.GEMINI, "gemini-2.0-flash", temperature=0.0),
    "A05": ModelConfig(ProviderType.OPENAI, "gpt-4o", temperature=0.1),
    "A06": ModelConfig(ProviderType.ANTHROPIC, "claude-3-5-sonnet-20241022", temperature=0.2),
    "A07": ModelConfig(ProviderType.OPENAI, "gpt-4o", temperature=0.0),
    "A08": ModelConfig(ProviderType.OPENAI, "gpt-4o", temperature=0.0),
    "A09": ModelConfig(ProviderType.OPENAI, "gpt-4o", temperature=0.0),
    "A10": ModelConfig(ProviderType.GEMINI, "gemini-2.0-flash", temperature=0.1),
    "A11": ModelConfig(ProviderType.GEMINI, "gemini-2.0-flash", temperature=0.1),
    "A12": ModelConfig(ProviderType.ANTHROPIC, "claude-3-5-sonnet-20241022", temperature=0.2),
    "A13": ModelConfig(ProviderType.GEMINI, "gemini-1.5-pro", temperature=0.3),
}


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0
    latency_seconds: float = 0.0
    parsed_json: Optional[Dict[str, Any]] = None
    mocked: bool = False


def _load_env_keys() -> Dict[str, str]:
    """Load API keys from system environment variables or standard dotenv file."""
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    return {
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", ""),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY", ""),
    }


class LLMRouter:
    """
    Multi-provider gateway that routes agent requests to Gemini, OpenAI, or Claude.
    Falls back gracefully to mock mode if API keys are absent.
    """

    def __init__(
        self,
        api_keys: Optional[Dict[str, str]] = None,
        default_provider: ProviderType = ProviderType.GEMINI,
        fallback_order: Optional[List[ProviderType]] = None,
    ):
        self.api_keys = api_keys or _load_env_keys()
        self.default_provider = default_provider
        self.fallback_order = fallback_order or [
            ProviderType.GEMINI,
            ProviderType.OPENAI,
            ProviderType.ANTHROPIC,
            ProviderType.MOCK,
        ]
        self.usage_history: List[LLMResponse] = []

    def set_api_key(self, provider: str, key: str) -> None:
        """Set or update an API key at runtime."""
        key_name = f"{provider.upper()}_API_KEY"
        self.api_keys[key_name] = key

    def dispatch(
        self,
        agent_id: str,
        system_prompt: str,
        user_prompt: str,
        context: Optional[Dict[str, Any]] = None,
        force_provider: Optional[ProviderType] = None,
    ) -> LLMResponse:
        """
        Dispatch prompt to the appropriate model based on agent routing configuration.
        """
        start_time = time.time()
        config = DEFAULT_MODEL_ROUTING.get(agent_id, ModelConfig(self.default_provider, "default-model"))

        target_provider = force_provider or config.provider

        # Attempt invocation through fallback chain if key is missing or call fails
        providers_to_try = [target_provider] + [p for p in self.fallback_order if p != target_provider]

        last_error = None
        for provider in providers_to_try:
            try:
                response = self._invoke_provider(
                    provider=provider,
                    model_name=config.model_name,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    context=context,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens,
                )
                response.latency_seconds = round(time.time() - start_time, 3)
                self.usage_history.append(response)
                return response
            except Exception as e:
                logger.warning(f"Provider '{provider.value}' failed for agent {agent_id}: {e}. Retrying fallback...")
                last_error = e

        # Final fallback to mock if everything fails
        logger.info(f"Using mock fallback for agent {agent_id}")
        mock_resp = self._generate_mock_response(agent_id, user_prompt)
        mock_resp.latency_seconds = round(time.time() - start_time, 3)
        self.usage_history.append(mock_resp)
        return mock_resp

    def _invoke_provider(
        self,
        provider: ProviderType,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        context: Optional[Dict[str, Any]],
        temperature: float,
        max_tokens: int,
    ) -> LLMResponse:
        """Invoke concrete LLM API client or raise Exception if unavailable."""

        if provider == ProviderType.GEMINI:
            key = self.api_keys.get("GEMINI_API_KEY")
            if not key:
                raise ValueError("GEMINI_API_KEY not configured")
            try:
                import google.generativeai as genai

                genai.configure(api_key=key)
                model = genai.GenerativeModel(
                    model_name=model_name if "gemini" in model_name else "gemini-1.5-pro",
                    system_instruction=system_prompt,
                )
                prompt_content = f"Context:\n{json.dumps(context or {})}\n\nTask:\n{user_prompt}"
                res = model.generate_content(
                    prompt_content,
                    generation_config=genai.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                )
                text = res.text
                prompt_tokens = len(prompt_content) // 4
                completion_tokens = len(text) // 4
                return LLMResponse(
                    content=text,
                    provider="gemini",
                    model=model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    estimated_cost_usd=round((prompt_tokens + completion_tokens) * 0.000002, 6),
                    parsed_json=self._try_parse_json(text),
                )
            except ImportError:
                raise RuntimeError("google-generativeai package not installed")

        elif provider == ProviderType.OPENAI:
            key = self.api_keys.get("OPENAI_API_KEY")
            if not key:
                raise ValueError("OPENAI_API_KEY not configured")
            try:
                import openai

                client = openai.OpenAI(api_key=key)
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context:\n{json.dumps(context or {})}\n\nTask:\n{user_prompt}"},
                ]
                res = client.chat.completions.create(
                    model=model_name if "gpt" in model_name else "gpt-4o",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                text = res.choices[0].message.content
                prompt_tokens = res.usage.prompt_tokens
                completion_tokens = res.usage.completion_tokens
                return LLMResponse(
                    content=text,
                    provider="openai",
                    model=model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=res.usage.total_tokens,
                    estimated_cost_usd=round((prompt_tokens * 0.000005) + (completion_tokens * 0.000015), 6),
                    parsed_json=self._try_parse_json(text),
                )
            except ImportError:
                raise RuntimeError("openai package not installed")

        elif provider == ProviderType.ANTHROPIC:
            key = self.api_keys.get("ANTHROPIC_API_KEY")
            if not key:
                raise ValueError("ANTHROPIC_API_KEY not configured")
            try:
                import anthropic

                client = anthropic.Anthropic(api_key=key)
                prompt_content = f"Context:\n{json.dumps(context or {})}\n\nTask:\n{user_prompt}"
                res = client.messages.create(
                    model=model_name if "claude" in model_name else "claude-3-5-sonnet-20241022",
                    max_tokens=max_tokens,
                    system=system_prompt,
                    messages=[{"role": "user", "content": prompt_content}],
                    temperature=temperature,
                )
                text = res.content[0].text
                prompt_tokens = res.usage.input_tokens
                completion_tokens = res.usage.output_tokens
                return LLMResponse(
                    content=text,
                    provider="anthropic",
                    model=model_name,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens,
                    estimated_cost_usd=round((prompt_tokens * 0.000003) + (completion_tokens * 0.000015), 6),
                    parsed_json=self._try_parse_json(text),
                )
            except ImportError:
                raise RuntimeError("anthropic package not installed")

        elif provider == ProviderType.MOCK:
            return self._generate_mock_response(agent_id=model_name, user_prompt=user_prompt)

        raise ValueError(f"Unsupported provider: {provider}")

    def _generate_mock_response(self, agent_id: str, user_prompt: str) -> LLMResponse:
        """Generate structured deterministic mock response when no API keys are present."""
        mock_payload = {
            "status": "completed",
            "agent_id": agent_id,
            "result": f"Simulated execution output for {agent_id}",
            "prompt_summary": user_prompt[:80],
            "quality_score": 0.95,
            "verification_passed": True,
        }
        content = json.dumps(mock_payload, indent=2)
        return LLMResponse(
            content=content,
            provider="mock",
            model="mock-simulator",
            prompt_tokens=50,
            completion_tokens=50,
            total_tokens=100,
            estimated_cost_usd=0.0,
            parsed_json=mock_payload,
            mocked=True,
        )

    def _try_parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract and parse embedded JSON code blocks or raw JSON string."""
        if not text:
            return None
        text_clean = text.strip()
        if "```json" in text_clean:
            try:
                json_str = text_clean.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            except Exception:
                pass
        elif "```" in text_clean:
            try:
                json_str = text_clean.split("```")[1].split("```")[0].strip()
                return json.loads(json_str)
            except Exception:
                pass
        try:
            return json.loads(text_clean)
        except Exception:
            return None

    def get_total_usage(self) -> Dict[str, Any]:
        """Aggregate token usage and cost metrics across all dispatches."""
        total_tokens = sum(r.total_tokens for r in self.usage_history)
        total_cost = sum(r.estimated_cost_usd for r in self.usage_history)
        return {
            "total_calls": len(self.usage_history),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 6),
            "calls_by_provider": {
                p: len([r for r in self.usage_history if r.provider == p])
                for p in set(r.provider for r in self.usage_history)
            },
        }
