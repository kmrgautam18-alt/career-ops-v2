"""
AI Model Abstraction Layer — Provider-Agnostic Interface.

Supports:
  - Google Gemini  (default, requires LLM_API_KEY)
  - OpenAI         (requires OPENAI_API_KEY)
  - Anthropic Claude (requires ANTHROPIC_API_KEY)

Usage:
    from backend.app.services.ai.models import get_model
    model = get_model("openai")   # or "gemini", "claude", or None for config default
    text = await model.generate("Hello")
    async for chunk in model.stream("Tell me a story"):
        print(chunk)
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import AsyncGenerator
from typing import Any, Protocol

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


# ==============================================================================
# Abstract Interface (Protocol)
# ==============================================================================


class AIModel(Protocol):
    """Protocol for AI model providers."""

    provider: str

    async def generate(self, prompt: str, system_instruction: str = "", **kwargs: Any) -> str:
        """Generate a complete text response."""
        ...

    async def generate_json(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """Generate a JSON response."""
        ...

    async def stream(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """Stream a text response token by token."""
        ...


# ==============================================================================
# Google Gemini Provider
# ==============================================================================


class GeminiModel:
    """Google Gemini AI provider."""

    provider = "gemini"

    def __init__(self) -> None:
        self._model = None
        self._initialized = False

    def _ensure_model(self) -> Any:
        if self._initialized:
            return self._model
        self._initialized = True

        api_key = settings.LLM_API_KEY or os.getenv("LLM_API_KEY", "")
        if not api_key:
            logger.warning("LLM_API_KEY not set. Gemini unavailable.")
            return None

        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(
                settings.LLM_MODEL or "gemini-2.0-flash",
                generation_config={
                    "temperature": 0.3,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 4096,
                },
            )
            return self._model
        except Exception as e:
            logger.error(f"Failed to init Gemini: {e}")
            return None

    async def generate(self, prompt: str, system_instruction: str = "", **kwargs: Any) -> str:
        model = self._ensure_model()
        if model is None:
            raise RuntimeError("Gemini model not available. Set LLM_API_KEY.")

        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [system_instruction]})
        contents.append({"role": "user", "parts": [prompt]})

        response = model.generate_content(contents)
        return response.text

    async def generate_json(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        text = await self.generate(prompt, system_instruction, **kwargs)
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    start = i + 1
                    break
            end = len(lines)
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().startswith("```"):
                    end = i
                    break
            text = "\n".join(lines[start:end]).strip()
        return json.loads(text)

    async def stream(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        model = self._ensure_model()
        if model is None:
            yield "data: " + json.dumps({"error": "Gemini not configured"}) + "\n\n"
            yield "data: [DONE]\n\n"
            return

        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [system_instruction]})
        contents.append({"role": "user", "parts": [prompt]})

        try:
            response = model.generate_content(contents, stream=True)
            for chunk in response:
                if chunk.text:
                    yield "data: " + json.dumps({"text": chunk.text}) + "\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Gemini stream error: {e}")
            yield "data: " + json.dumps({"error": str(e)}) + "\n\n"
            yield "data: [DONE]\n\n"


# ==============================================================================
# OpenAI Provider
# ==============================================================================


class OpenAIModel:
    """OpenAI AI provider."""

    provider = "openai"

    def __init__(self) -> None:
        self._client = None
        self._initialized = False

    def _ensure_client(self) -> Any:
        if self._initialized:
            return self._client
        self._initialized = True

        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            logger.warning("OPENAI_API_KEY not set. OpenAI unavailable.")
            return None

        try:
            from openai import AsyncOpenAI

            self._client = AsyncOpenAI(api_key=api_key)
            return self._client
        except Exception as e:
            logger.error(f"Failed to init OpenAI: {e}")
            return None

    async def generate(self, prompt: str, system_instruction: str = "", **kwargs: Any) -> str:
        client = self._ensure_client()
        if client is None:
            raise RuntimeError("OpenAI client not available. Set OPENAI_API_KEY.")

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=kwargs.get("model", "gpt-4o-mini"),
            messages=messages,
            temperature=kwargs.get("temperature", 0.3),
            max_tokens=kwargs.get("max_tokens", 4096),
        )
        return response.choices[0].message.content or ""  # type: ignore[no-any-return]

    async def generate_json(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        text = await self.generate(prompt, system_instruction, **kwargs)
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    start = i + 1
                    break
            end = len(lines)
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().startswith("```"):
                    end = i
                    break
            text = "\n".join(lines[start:end]).strip()
        return json.loads(text)

    async def stream(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        client = self._ensure_client()
        if client is None:
            yield "data: " + json.dumps({"error": "OpenAI not configured"}) + "\n\n"
            yield "data: [DONE]\n\n"
            return

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = await client.chat.completions.create(
                model=kwargs.get("model", "gpt-4o-mini"),
                messages=messages,
                stream=True,
                temperature=kwargs.get("temperature", 0.3),
                max_tokens=kwargs.get("max_tokens", 4096),
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield "data: " + json.dumps({"text": chunk.choices[0].delta.content}) + "\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            yield "data: " + json.dumps({"error": str(e)}) + "\n\n"
            yield "data: [DONE]\n\n"


# ==============================================================================
# Anthropic Claude Provider
# ==============================================================================


class ClaudeModel:
    """Anthropic Claude AI provider."""

    provider = "claude"

    def __init__(self) -> None:
        self._client = None
        self._initialized = False

    def _ensure_client(self) -> Any:
        if self._initialized:
            return self._client
        self._initialized = True

        api_key = os.getenv("ANTHROPIC_API_KEY", "")
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not set. Claude unavailable.")
            return None

        try:
            from anthropic import AsyncAnthropic

            self._client = AsyncAnthropic(api_key=api_key)
            return self._client
        except Exception as e:
            logger.error(f"Failed to init Claude: {e}")
            return None

    async def generate(self, prompt: str, system_instruction: str = "", **kwargs: Any) -> str:
        client = self._ensure_client()
        if client is None:
            raise RuntimeError("Claude client not available. Set ANTHROPIC_API_KEY.")

        response = await client.messages.create(
            model=kwargs.get("model", "claude-3-haiku-20240307"),
            max_tokens=kwargs.get("max_tokens", 4096),
            system=system_instruction or None,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text if response.content else ""  # type: ignore[no-any-return]

    async def generate_json(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        text = await self.generate(prompt, system_instruction, **kwargs)
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            start = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("```"):
                    start = i + 1
                    break
            end = len(lines)
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].strip().startswith("```"):
                    end = i
                    break
            text = "\n".join(lines[start:end]).strip()
        return json.loads(text)

    async def stream(
        self, prompt: str, system_instruction: str = "", **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        client = self._ensure_client()
        if client is None:
            yield "data: " + json.dumps({"error": "Claude not configured"}) + "\n\n"
            yield "data: [DONE]\n\n"
            return

        try:
            async with client.messages.stream(
                model=kwargs.get("model", "claude-3-haiku-20240307"),
                max_tokens=kwargs.get("max_tokens", 4096),
                system=system_instruction or None,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                async for text in stream.text_stream:
                    yield "data: " + json.dumps({"text": text}) + "\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Claude stream error: {e}")
            yield "data: " + json.dumps({"error": str(e)}) + "\n\n"
            yield "data: [DONE]\n\n"


# ==============================================================================
# Provider Registry & Factory
# ==============================================================================

_PROVIDER_REGISTRY: dict[str, type] = {
    "gemini": GeminiModel,
    "google": GeminiModel,
    "openai": OpenAIModel,
    "claude": ClaudeModel,
    "anthropic": ClaudeModel,
}

_provider_cache: dict[str, GeminiModel | OpenAIModel | ClaudeModel] = {}


def get_model(provider: str | None = None) -> GeminiModel | OpenAIModel | ClaudeModel:
    """
    Get an AI model instance by provider name.

    Args:
        provider: "gemini", "openai", or "claude". If None, uses config default.

    Returns:
        An AI model instance (GeminiModel, OpenAIModel, or ClaudeModel).

    Raises:
        ValueError: If the provider is unknown.
    """
    provider = provider or settings.LLM_PROVIDER or "google"
    provider = provider.lower().strip()

    if provider in _provider_cache:
        return _provider_cache[provider]

    model_cls = _PROVIDER_REGISTRY.get(provider)
    if model_cls is None:
        available = ", ".join(sorted(set(_PROVIDER_REGISTRY.keys())))
        raise ValueError(f"Unknown AI provider: '{provider}'. Available: {available}")

    instance = model_cls()
    _provider_cache[provider] = instance
    return instance


def register_provider(name: str, model_cls: type) -> None:
    """Register a custom AI provider."""
    _PROVIDER_REGISTRY[name] = model_cls
