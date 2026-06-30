import re
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
SECTION_HEADINGS = {
    "professional summary": "summary",
    "summary": "summary",
    "top strengths": "strengths",
    "strengths": "strengths",
    "weaknesses": "weaknesses",
    "resume improvement recommendations": "recommendations",
    "recommendations": "recommendations",
}
MARKDOWN_RULE_PATTERN = re.compile(r"^\s*[-*_]{3,}\s*$")
ORDERED_LIST_PATTERN = re.compile(r"^\d+[\.)]\s+")
UNORDERED_LIST_PATTERN = re.compile(r"^[-*+]\s+")


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

        return self._parse_response_text(self._extract_response_text(response))

    async def _generate_content(self, prompt: str) -> object:
        genai = self._load_genai_module()
        client_factory = cast(Callable[..., object], getattr(genai, "Client"))
        client = client_factory(api_key=self.api_key)
        async_client = getattr(client, "aio")
        models = getattr(async_client, "models")
        generate_content = cast(
            Callable[..., Awaitable[object]],
            getattr(models, "generate_content"),
        )

        return await generate_content(model=self.model, contents=prompt)

    def _load_genai_module(self) -> ModuleType:
        try:
            return import_module("google.genai")
        except ImportError as exc:
            raise AIProviderConfigurationError(
                "Google Gen AI SDK is not installed."
            ) from exc

    def _extract_response_text(self, response: object) -> str:
        text = getattr(response, "text", "")
        if isinstance(text, str):
            return text.strip()
        return ""

    def _parse_response_text(self, text: str) -> AIAnalysis:
        sections: dict[str, list[str]] = {
            "summary": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
        }
        fallback_summary: list[str] = []
        current_section: str | None = None

        for raw_line in text.splitlines():
            cleaned_line = self._clean_markdown_line(raw_line)
            if not cleaned_line:
                continue

            heading, inline_content = self._extract_heading(cleaned_line)
            if heading is not None:
                current_section = heading
                if inline_content:
                    sections[current_section].append(inline_content)
                continue

            if current_section is None:
                fallback_summary.append(cleaned_line)
                continue

            sections[current_section].append(cleaned_line)

        summary = " ".join(sections["summary"]).strip()
        if not summary:
            summary = " ".join(fallback_summary).strip() or DEFAULT_AI_SUMMARY

        return AIAnalysis(
            summary=summary,
            strengths=sections["strengths"],
            weaknesses=sections["weaknesses"],
            recommendations=sections["recommendations"],
        )

    def _extract_heading(self, line: str) -> tuple[str | None, str]:
        normalized_line = self._normalize_heading(line)
        section = SECTION_HEADINGS.get(normalized_line)
        if section is not None:
            return section, ""

        heading_text, separator, inline_content = line.partition(":")
        if not separator:
            return None, ""

        section = SECTION_HEADINGS.get(self._normalize_heading(heading_text))
        if section is None:
            return None, ""

        return section, self._clean_markdown_line(inline_content)

    def _normalize_heading(self, line: str) -> str:
        normalized = line.strip().strip(":")
        normalized = normalized.replace("*", "").replace("_", "")
        normalized = normalized.strip()
        return " ".join(normalized.lower().split())

    def _clean_markdown_line(self, line: str) -> str:
        if MARKDOWN_RULE_PATTERN.fullmatch(line):
            return ""

        cleaned = line.strip()
        cleaned = cleaned.removeprefix("#").lstrip("#").strip()
        cleaned = UNORDERED_LIST_PATTERN.sub("", cleaned)
        cleaned = ORDERED_LIST_PATTERN.sub("", cleaned)
        cleaned = cleaned.replace("**", "").replace("__", "")
        cleaned = cleaned.strip("`").strip()
        return cleaned
