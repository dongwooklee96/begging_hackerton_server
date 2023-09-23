from typing import Optional

from fastapi import APIRouter, Depends
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from src.auth.auth import generate_access_token, SECRET_KEY, ALGORITHM
from src.user.application.user import UserService
from src.user.repository.users import UserRepository

auth_router = APIRouter(
    tags=["Auth"],
)


class LoginRequest(BaseModel):
    id: int
    nickname: str
    profile_url: Optional[str] = None


@auth_router.post("/login/kakao")
async def kakao_login(req: LoginRequest, session: AsyncSession = Depends(get_session)):
    """
    로그인 정보로 로그인 한다.
    """
    user_service = UserService(user_repository=UserRepository(session=session))
    user = await user_service.get_user_by_id(id=req.id)
    if not user:
        user = await user_service.create_user(
            id=req.id, nickname=req.nickname, profile_url=req.profile_url
        )
    await session.commit()
    token = await generate_access_token(user_key=user.user_key)
    payload = jwt.decode(token["access_token"], SECRET_KEY, algorithms=[ALGORITHM])

    return {"access_token": await generate_access_token(user_key=user.user_key)}
