from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from database.models import User, ProductGame
from src.auth.auth import get_current_active_user

game_router = APIRouter(
    tags=["Game"],
)


@game_router.get("/join")
async def join_game(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 게임에 조인한다.
    """
    ProductGame()
