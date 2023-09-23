from src.user.repository.users import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, id: int, nickname: str, profile_url: str):
        """
        유저를 생성한다.
        """
        return await self.user_repository.create_user(
            id=id, nickname=nickname, profile_url=profile_url
        )

    async def get_user_by_id(self, id: int):
        """
        유저를 유저 아이디로 조회한다.
        """
        return await self.user_repository.get_user_by_id(id=id)

    async def get_user_by_user_key(self, user_key: int):
        """
        유저를 유저 키로 조회한다.
        """
        return await self.user_repository.get_user_by_user_key(user_key=user_key)
