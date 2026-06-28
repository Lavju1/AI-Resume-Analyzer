import asyncio
from pathlib import Path

from docx import Document

from ai_resume_analyzer.parsers.base import BaseResumeParser


class DocxResumeParser(BaseResumeParser):
    async def parse(self, file_path: Path) -> str:
        return await asyncio.to_thread(self._extract_text, file_path)

    def _extract_text(self, file_path: Path) -> str:
        document = Document(str(file_path))
        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]
        return "\n".join(paragraphs)
