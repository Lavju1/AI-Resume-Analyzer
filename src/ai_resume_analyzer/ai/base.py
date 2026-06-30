from abc import ABC, abstractmethod

from ai_resume_analyzer.ai.schemas import AIAnalysis


class BaseAIProvider(ABC):
    @abstractmethod
    async def analyze_resume(
        self,
        *,
        prompt: str,
    ) -> AIAnalysis:
        raise NotImplementedError
