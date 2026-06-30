from ai_resume_analyzer.ai.base import BaseAIProvider


class AIProviderFactory:
    def get_provider(self) -> BaseAIProvider:
        raise NotImplementedError("No AI provider has been configured.")
