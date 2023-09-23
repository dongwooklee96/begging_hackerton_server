from database.models import User
from src.user.repository.users import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, nickname: str, email: str):
        """
        유저를 생성한다.
        """
        return await self.user_repository.create_user(nickname=nickname, email=email)

    async def get_user_by_email(self, email: str) -> User:
        """
        유저를 유저 이메일로 조회한다.
        """
        return await self.user_repository.get_user_by_email(email=email)
