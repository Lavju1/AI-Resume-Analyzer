from collections.abc import Awaitable, Callable
from importlib import import_module
from types import ModuleType
from typing import cast

from ai_resume_analyzer.ai.base import BaseAIProvider
from ai_resume_analyzer.ai.exceptions import (
    AIProviderConfigurationError,
    AIProviderError,
)
from ai_resume_analyzer.ai.schemas import AIAnalysis

DEFAULT_AI_SUMMARY = "No AI summary was returned."


class GeminiProvider(BaseAIProvider):
    def __init__(self, *, api_key: str, model: str) -> None:
        normalized_api_key = api_key.strip()
        if not normalized_api_key:
            raise AIProviderConfigurationError("GEMINI_API_KEY must be configured.")

        self.api_key = normalized_api_key
        self.model = model

    async def analyze_resume(
        self,
        *,
        prompt: str,
    ) -> AIAnalysis:
        try:
            response = await self._generate_content(prompt)
        except AIProviderError:
            raise
        except Exception as exc:
            raise AIProviderError("Gemini provider failed to analyze resume.") from exc

        return AIAnalysis(
            summary=self._extract_response_text(response) or DEFAULT_AI_SUMMARY,
            strengths=[],
            weaknesses=[],
            recommendations=[],
        )

    async def _generate_content(self, prompt: str) -> object:
        genai = self._load_genai_module()
        configure = cast(Callable[..., None], genai.configure)
        generative_model = cast(
            Callable[[str], object],
            genai.GenerativeModel,
        )

        configure(api_key=self.api_key)
        model = generative_model(self.model)

        generate_content_async = cast(
            Callable[[str], Awaitable[object]],
            model.generate_content_async,  # type: ignore[attr-defined]
        )
        return await generate_content_async(prompt)

    def _load_genai_module(self) -> ModuleType:
        try:
            return import_module("google.generativeai")
        except ImportError as exc:
            raise AIProviderConfigurationError(
                "Google Generative AI SDK is not installed."
            ) from exc

    def _extract_response_text(self, response: object) -> str:
        text = getattr(response, "text", "")
        if isinstance(text, str):
            return text.strip()
        return ""
