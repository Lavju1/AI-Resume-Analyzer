from ai_resume_analyzer.extractors.regex_extractor import RegexResumeExtractor
from ai_resume_analyzer.extractors.schemas import ResumeData


class ResumeExtractionService:
    def __init__(self, extractor: RegexResumeExtractor | None = None) -> None:
        self.extractor = extractor or RegexResumeExtractor()

    def extract_resume_data(self, text: str) -> ResumeData:
        return self.extractor.extract(text)
