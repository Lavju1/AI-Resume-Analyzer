from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_resume_analyzer.database.models.user import User
from ai_resume_analyzer.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session, model=User)

    async def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.session.scalars(statement)
        return result.one_or_none()

    async def create_user(
        self,
        *,
        email: str,
        hashed_password: str,
        is_active: bool = True,
    ) -> User:
        return await self.create(
            {
                "email": email,
                "hashed_password": hashed_password,
                "is_active": is_active,
            }
        )
