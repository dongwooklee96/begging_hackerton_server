from datetime import datetime

from sqlmodel import select

from database.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def create_user(self, id, nickname, profile_url):
        """
        이메일로 유저를 생성한다.
        """
        user = User(
            id=id,
            nickname=nickname,
            profile_url=profile_url,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def get_user_by_id(self, id: int):
        """
        아이디와 일치하는 유저를 반환한다.
        """
        statement = select(User).where(User.id == id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_id(self, id: int):
        """
        아이디와 일치하는 유저를 반환한다.
        """
        statement = select(User).where(User.id == id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_user_key(self, user_key: int):
        """
        유저를 유저 키로 조회한다.
        """
        statement = select(User).where(User.user_key == user_key)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user
