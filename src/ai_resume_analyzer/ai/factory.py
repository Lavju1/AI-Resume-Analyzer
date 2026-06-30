from ai_resume_analyzer.ai.base import BaseAIProvider
from ai_resume_analyzer.ai.exceptions import AIProviderConfigurationError
from ai_resume_analyzer.ai.gemini_provider import GeminiProvider
from ai_resume_analyzer.config import Settings, get_settings


class AIProviderFactory:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def get_provider(self) -> BaseAIProvider:
        if self.settings.gemini_api_key is None:
            raise AIProviderConfigurationError("GEMINI_API_KEY must be configured.")

        return GeminiProvider(
            api_key=self.settings.gemini_api_key,
            model=self.settings.gemini_model,
        )
