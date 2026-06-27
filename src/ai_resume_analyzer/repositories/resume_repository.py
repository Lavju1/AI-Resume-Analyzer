from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_resume_analyzer.constants.uploads import UPLOAD_STATUS_PENDING
from ai_resume_analyzer.database.models.resume import Resume
from ai_resume_analyzer.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=Resume)

    async def create_resume(
        self,
        *,
        user_id: UUID,
        original_filename: str,
        stored_filename: str,
        content_type: str,
        file_size: int,
        storage_path: str,
        upload_status: str = UPLOAD_STATUS_PENDING,
    ) -> Resume:
        return await self.create(
            {
                "user_id": user_id,
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "content_type": content_type,
                "file_size": file_size,
                "storage_path": storage_path,
                "upload_status": upload_status,
            }
        )

    async def get_by_id(self, entity_id: UUID) -> Resume | None:
        return await super().get_by_id(entity_id)

    async def get_all_by_user(
        self,
        user_id: UUID,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Resume]:
        statement = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.scalars(statement)
        return list(result.all())
