from abc import ABC, abstractmethod

from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.job_matching.schemas import (
    JobDescription,
    JobMatchResult,
)


class BaseJobMatcher(ABC):
    @abstractmethod
    def match(
        self,
        *,
        resume_data: ResumeData,
        job_description: JobDescription,
    ) -> JobMatchResult:
        raise NotImplementedError
