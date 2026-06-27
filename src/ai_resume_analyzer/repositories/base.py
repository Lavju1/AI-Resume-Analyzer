from collections.abc import Mapping
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_resume_analyzer.database.models.base import BaseModel


class BaseRepository[ModelT: BaseModel]:
    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, entity_id: UUID) -> ModelT | None:
        return await self.session.get(self.model, entity_id)

    async def get_all(self, *, offset: int = 0, limit: int = 100) -> list[ModelT]:
        statement = select(self.model).offset(offset).limit(limit)
        result = await self.session.scalars(statement)
        return list(result.all())

    async def create(self, data: Mapping[str, Any]) -> ModelT:
        entity = self.model()
        self._apply_data(entity, data)

        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)

        return entity

    async def update(self, entity: ModelT, data: Mapping[str, Any]) -> ModelT:
        self._apply_data(entity, data)

        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)

        return entity

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
        await self.session.flush()

    def _apply_data(self, entity: ModelT, data: Mapping[str, Any]) -> None:
        for field, value in data.items():
            setattr(entity, field, value)
