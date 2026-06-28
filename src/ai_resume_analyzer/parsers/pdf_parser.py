import asyncio
from pathlib import Path

import fitz

from ai_resume_analyzer.parsers.base import BaseResumeParser


class PDFResumeParser(BaseResumeParser):
    async def parse(self, file_path: Path) -> str:
        return await asyncio.to_thread(self._extract_text, file_path)

    def _extract_text(self, file_path: Path) -> str:
        with fitz.open(file_path) as document:
            page_text = [page.get_text() for page in document]
        return "\n".join(text for text in page_text if text.strip())
