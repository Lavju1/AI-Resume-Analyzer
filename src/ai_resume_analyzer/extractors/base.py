from abc import ABC, abstractmethod

from ai_resume_analyzer.extractors.schemas import ResumeData


class BaseResumeExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> ResumeData:
        raise NotImplementedError
