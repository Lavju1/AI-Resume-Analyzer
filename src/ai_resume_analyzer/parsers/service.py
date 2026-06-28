from pathlib import Path

from ai_resume_analyzer.parsers.factory import ResumeParserFactory


class ResumeParserService:
    def __init__(self, factory: ResumeParserFactory | None = None) -> None:
        self.factory = factory or ResumeParserFactory()

    async def parse_resume(self, file_path: Path) -> str:
        parser = self.factory.get_parser(file_path)
        return await parser.parse(file_path)
