from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ai_resume_analyzer.auth.dependencies import get_auth_service, get_current_user
from ai_resume_analyzer.database.models.user import User
from ai_resume_analyzer.schemas.auth import Token, UserLogin, UserRead, UserRegister
from ai_resume_analyzer.services.auth_service import (
    AuthService,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data: UserRegister,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserRead:
    try:
        user = await auth_service.register_user(data)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        ) from exc
    return UserRead.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login_user(
    data: UserLogin,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:
    try:
        return await auth_service.authenticate_user(data)
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserRead:
    return UserRead.model_validate(current_user)
