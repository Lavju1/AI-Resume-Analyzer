from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from ai_resume_analyzer.auth.jwt import decode_access_token
from ai_resume_analyzer.database.session import get_db
from ai_resume_analyzer.repositories.user_repository import UserRepository
from ai_resume_analyzer.schemas.auth import TokenPayload
from ai_resume_analyzer.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(user_repository=user_repository)


async def get_token_payload(
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> TokenPayload | None:
    if token is None:
        return None

    try:
        return decode_access_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
