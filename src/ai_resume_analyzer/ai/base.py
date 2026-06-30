from abc import ABC, abstractmethod

from ai_resume_analyzer.ai.schemas import AIAnalysis
from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.feedback.schemas import ResumeFeedback
from ai_resume_analyzer.scoring.schemas import ATSScore


class BaseAIProvider(ABC):
    @abstractmethod
    async def analyze_resume(
        self,
        *,
        parsed_text: str,
        extracted_data: ResumeData,
        ats_score: ATSScore,
        feedback: ResumeFeedback,
    ) -> AIAnalysis:
        raise NotImplementedError
