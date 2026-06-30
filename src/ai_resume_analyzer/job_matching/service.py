from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.job_matching.base import BaseJobMatcher
from ai_resume_analyzer.job_matching.matcher import RuleBasedJobMatcher
from ai_resume_analyzer.job_matching.schemas import (
    JobDescription,
    JobMatchResult,
)


class JobMatchingService:
    def __init__(self, matcher: BaseJobMatcher | None = None) -> None:
        self.matcher = matcher or RuleBasedJobMatcher()

    def match(
        self,
        *,
        resume_data: ResumeData,
        job_description: JobDescription,
    ) -> JobMatchResult:
        return self.matcher.match(
            resume_data=resume_data,
            job_description=job_description,
        )
