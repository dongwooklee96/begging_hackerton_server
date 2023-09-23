from sqlmodel import select

from database.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def create_user(self, nickname, email):
        """
        이메일로 유저를 생성한다.
        """
        user = User(
            nickname=nickname,
            email=email,
            deleted=False,
        )
        self.session.add(user)
        self.session.commit()
        return user

    async def get_user_by_email(self, email):
        """
        이메일에 일치하는 유저를 반환한다.
        """
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user
