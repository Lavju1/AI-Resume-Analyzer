from ai_resume_analyzer.repositories.user_repository import UserRepository
from ai_resume_analyzer.schemas.auth import UserLogin, UserRegister


class AuthService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def register_user(self, data: UserRegister) -> None:
        raise NotImplementedError("Registration will be implemented in a future phase.")

    async def authenticate_user(self, data: UserLogin) -> None:
        raise NotImplementedError("Login will be implemented in a future phase.")
