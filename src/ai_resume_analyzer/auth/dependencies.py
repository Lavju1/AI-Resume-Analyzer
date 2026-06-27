from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from ai_resume_analyzer.auth.jwt import decode_access_token
from ai_resume_analyzer.database.models.user import User
from ai_resume_analyzer.database.session import get_db
from ai_resume_analyzer.repositories.user_repository import UserRepository
from ai_resume_analyzer.schemas.auth import TokenPayload
from ai_resume_analyzer.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)


def _unauthorized_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


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
    except (InvalidTokenError, ValidationError) as exc:
        raise _unauthorized_exception() from exc


async def get_current_user(
    token_payload: Annotated[TokenPayload | None, Depends(get_token_payload)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    if token_payload is None:
        raise _unauthorized_exception()

    try:
        user_id = UUID(token_payload.subject)
    except ValueError as exc:
        raise _unauthorized_exception() from exc

    user = await user_repository.get_by_id(user_id)
    if user is None or not user.is_active:
        raise _unauthorized_exception()

    return user
