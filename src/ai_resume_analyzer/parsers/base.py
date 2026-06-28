from abc import ABC, abstractmethod
from pathlib import Path


class BaseResumeParser(ABC):
    @abstractmethod
    async def parse(self, file_path: Path) -> str:
        raise NotImplementedError
