"""Database repository abstractions."""

from ai_resume_analyzer.repositories.base import BaseRepository
from ai_resume_analyzer.repositories.resume_repository import ResumeRepository
from ai_resume_analyzer.repositories.user_repository import UserRepository

__all__ = ["BaseRepository", "ResumeRepository", "UserRepository"]
