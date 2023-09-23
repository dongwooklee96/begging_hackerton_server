from select import select
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from database.models import User, UserGame, Game
from src.auth.auth import get_current_active_user

user_router = APIRouter(
    tags=["User"],
)


@user_router.get("/take/history")
async def take_history(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 띱(가져간)한 내역을 조회한다.
    """
    statement = select(UserGame).where(UserGame.user_key == current_user.user_key)
    results = await session.execute(statement)
    user_games = results.all()
    return user_games


@user_router.get("/give/history")
async def give_history(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 나눔한 내역을 조회한다.
    """
    statement = select(Game).where(Game.user_key == current_user.user_key)
    results = await session.execute(statement)
    user_games = results.all()
    return user_games
