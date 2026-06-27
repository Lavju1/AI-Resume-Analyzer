from sqlalchemy.exc import IntegrityError

from ai_resume_analyzer.auth.jwt import create_access_token
from ai_resume_analyzer.auth.security import hash_password, verify_password
from ai_resume_analyzer.database.models.user import User
from ai_resume_analyzer.repositories.user_repository import UserRepository
from ai_resume_analyzer.schemas.auth import Token, UserLogin, UserRegister


class EmailAlreadyExistsError(Exception):
    """Raised when a registration email already belongs to an existing user."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials cannot be validated."""


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def register_user(self, data: UserRegister) -> User:
        existing_user = await self.user_repository.get_by_email(str(data.email))
        if existing_user is not None:
            raise EmailAlreadyExistsError

        hashed_password = hash_password(data.password)

        try:
            user = await self.user_repository.create_user(
                email=str(data.email),
                hashed_password=hashed_password,
            )
            await self.user_repository.session.commit()
        except IntegrityError as exc:
            await self.user_repository.session.rollback()
            raise EmailAlreadyExistsError from exc

        return user

    async def authenticate_user(self, data: UserLogin) -> Token:
        user = await self.user_repository.get_by_email(str(data.email))
        if user is None or not user.is_active:
            raise InvalidCredentialsError

        if not verify_password(data.password, user.hashed_password):
            raise InvalidCredentialsError

        access_token = create_access_token(subject=str(user.id))
        return Token(access_token=access_token)
