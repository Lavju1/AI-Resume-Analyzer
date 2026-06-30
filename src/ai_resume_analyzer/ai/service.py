from ai_resume_analyzer.ai.base import BaseAIProvider
from ai_resume_analyzer.ai.factory import AIProviderFactory
from ai_resume_analyzer.ai.schemas import AIAnalysis
from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.feedback.schemas import ResumeFeedback
from ai_resume_analyzer.scoring.schemas import ATSScore


class AIAnalysisService:
    def __init__(self, provider: BaseAIProvider | None = None) -> None:
        self.provider = provider or AIProviderFactory().get_provider()

    async def analyze_resume(
        self,
        *,
        parsed_text: str,
        extracted_data: ResumeData,
        ats_score: ATSScore,
        feedback: ResumeFeedback,
    ) -> AIAnalysis:
        prompt = self._build_prompt(
            parsed_text=parsed_text,
            extracted_data=extracted_data,
            ats_score=ats_score,
            feedback=feedback,
        )
        return await self.provider.analyze_resume(prompt=prompt)

    def _build_prompt(
        self,
        *,
        parsed_text: str,
        extracted_data: ResumeData,
        ats_score: ATSScore,
        feedback: ResumeFeedback,
    ) -> str:
        skills = self._format_list(extracted_data.skills)
        education = self._format_list(extracted_data.education)
        experience = self._format_list(extracted_data.experience)
        projects = self._format_list(extracted_data.projects)
        deterministic_feedback = self._format_feedback(feedback)

        return (
            "Analyze this resume and return a professional summary, top strengths, "
            "weaknesses, and resume improvement recommendations.\n\n"
            "Parsed resume text:\n"
            f"{parsed_text}\n\n"
            "Extracted contact information:\n"
            f"Name: {extracted_data.name or 'Not found'}\n"
            f"Email: {extracted_data.email or 'Not found'}\n"
            f"Phone: {extracted_data.phone or 'Not found'}\n\n"
            "Skills:\n"
            f"{skills}\n\n"
            "Education:\n"
            f"{education}\n\n"
            "Experience:\n"
            f"{experience}\n\n"
            "Projects:\n"
            f"{projects}\n\n"
            "ATS score:\n"
            f"{ats_score.overall_score}\n\n"
            "Existing deterministic feedback:\n"
            f"{deterministic_feedback}\n"
        )

    def _format_list(self, values: list[str]) -> str:
        if not values:
            return "Not found"
        return "\n".join(f"- {value}" for value in values)

    def _format_feedback(self, feedback: ResumeFeedback) -> str:
        if not feedback.feedback:
            return feedback.overall_summary

        feedback_items = [
            (f"- [{item.severity}] {item.category}: " f"{item.title} {item.message}")
            for item in feedback.feedback
        ]
        return "\n".join([feedback.overall_summary, *feedback_items])
