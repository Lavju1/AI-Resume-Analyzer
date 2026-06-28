from pathlib import Path

from ai_resume_analyzer.parsers.base import BaseResumeParser
from ai_resume_analyzer.parsers.docx_parser import DocxResumeParser
from ai_resume_analyzer.parsers.exceptions import UnsupportedResumeFormatError
from ai_resume_analyzer.parsers.pdf_parser import PDFResumeParser


class ResumeParserFactory:
    def get_parser(self, file_path: Path) -> BaseResumeParser:
        extension = file_path.suffix.lower()

        if extension == ".pdf":
            return PDFResumeParser()
        if extension == ".docx":
            return DocxResumeParser()

        msg = f"Unsupported resume format: {extension or 'unknown'}"
        raise UnsupportedResumeFormatError(msg)
