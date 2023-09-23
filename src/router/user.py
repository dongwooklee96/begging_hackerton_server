from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from database.models import User
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
    statement = text(
        f"""
        select c.category_name, p.title, ug.is_winner
        from user_game as ug
        join game as g on g.game_key = ug.game_key
        join product as p on p.product_key = g.product_key
        join category as c on c.category = p.category_key
        where 1 = 1
        and ug.user_key = {current_user.user_key}
        """
    )
    results = await session.execute(statement)
    user_games = results.fetchall()
    return user_games


@user_router.get("/give/history")
async def give_history(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 나눔한 내역을 조회한다.
    """
    statement = text(
        """
        select p.title, p.product_key, ug.is_winner
        from user_game as ug
        join game as g on g.user_key = ug.user_key
        join product as p on p.product_key = g.product_key
        where user_key = 4
        """
    )
    results = await session.execute(statement)
    user_games = results.all()
    return user_games
