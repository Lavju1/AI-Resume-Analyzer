from ai_resume_analyzer.ai import AIAnalysis, AIAnalysisService
from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.job_matching.schemas import (
    JobDescription,
    JobMatchResult,
)


class AIJobMatchingService:
    def __init__(
        self,
        ai_analysis_service: AIAnalysisService | None = None,
    ) -> None:
        self.ai_analysis_service = ai_analysis_service or AIAnalysisService()

    async def analyze_job_match(
        self,
        *,
        parsed_text: str,
        resume_data: ResumeData,
        job_description: JobDescription,
        job_match: JobMatchResult,
    ) -> AIAnalysis:
        prompt = self._build_prompt(
            parsed_text=parsed_text,
            resume_data=resume_data,
            job_description=job_description,
            job_match=job_match,
        )
        return await self.ai_analysis_service.provider.analyze_resume(prompt=prompt)

    def _build_prompt(
        self,
        *,
        parsed_text: str,
        resume_data: ResumeData,
        job_description: JobDescription,
        job_match: JobMatchResult,
    ) -> str:
        return (
            "Analyze how well this resume matches the job description. "
            "Return an overall job fit summary, resume strengths for this role, "
            "missing qualifications, and recommendations to improve the resume "
            "for this specific job.\n\n"
            "Resume text:\n"
            f"{parsed_text}\n\n"
            "Resume skills:\n"
            f"{self._format_list(resume_data.skills)}\n\n"
            "Job description:\n"
            f"{job_description.text}\n\n"
            "Match percentage:\n"
            f"{job_match.overall_match}\n\n"
            "Matched skills:\n"
            f"{self._format_list(job_match.matched_skills)}\n\n"
            "Missing skills:\n"
            f"{self._format_list(job_match.missing_skills)}\n\n"
            "Matched keywords:\n"
            f"{self._format_list(job_match.matched_keywords)}\n\n"
            "Missing keywords:\n"
            f"{self._format_list(job_match.missing_keywords)}\n"
        )

    def _format_list(self, values: list[str]) -> str:
        if not values:
            return "Not found"
        return "\n".join(f"- {value}" for value in values)
