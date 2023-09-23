from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.responses import JSONResponse

from database.connection import get_session
from database.models import Game, User, UserGame, Product
from src.auth.auth import get_current_active_user

game_router = APIRouter(
    tags=["Game"],
)


@game_router.post("/join/{product_key}")
async def join_game(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_key: int,
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 게임에 조인한다.
    """
    statement = select(Game).where(Game.product_key == product_key)
    result = await session.execute(statement)
    game = result.scalar_one_or_none()
    if not game:
        return JSONResponse(content={"message": "게임이 존재하지 않습니다."}, status_code=400)
    # 이미 게임에 참여하고 있는 경우에는 에러를 리턴한다.
    statement = (
        select(UserGame)
        .where(UserGame.user_key == current_user.user_key)
        .where(UserGame.game_key == game.game_key)
    )
    result = await session.execute(statement)
    user_game = result.all()
    if len(user_game) > 0:
        return JSONResponse(
            content={"message": "해당 유저는 이미 게임에 참여하고 있습니다."}, status_code=400
        )

    # 게임에 참여한 유저가 최대 숫자라면 참여할 수 없다.
    statement = select(UserGame).where(UserGame.game_key == game.game_key)
    result = await session.execute(statement)
    user_game = result.all()

    statement = select(Product).where(Product.product_key == product_key)
    result = await session.execute(statement)
    product = result.scalar_one_or_none()

    if len(user_game) >= product.max_participants:
        return JSONResponse(
            content={"message": "해당 게임은 이미 최대 인원이 참여하고 있습니다."}, status_code=400
        )

    user_game = UserGame(user_key=current_user.user_key, game_key=game.game_key)
    session.add(user_game)
    await session.commit()
    return JSONResponse(content={"message": "success"}, status_code=201)


@game_router.delete("/quit/{product_key}")
async def quit_game(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_key: int,
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 게임에서 나온다.
    """
    statement = select(Game).where(Game.product_key == product_key)
    result = await session.execute(statement)
    game = result.scalar_one_or_none()
    if not game:
        return JSONResponse(content={"message": "게임이 존재하지 않습니다."}, status_code=400)
    # 게임에 참여하고 있지 않은 경우에는 에러를 리턴한다.
    statement = (
        select(UserGame)
        .where(UserGame.user_key == current_user.user_key)
        .where(UserGame.game_key == game.game_key)
    )
    result = await session.execute(statement)
    current_user_joined_game = result.all()
    if len(current_user_joined_game) == 0:
        return JSONResponse(
            content={"message": "해당 유저는 게임에 참여하고 있지 않습니다."}, status_code=400
        )

    statement = delete(UserGame).where(UserGame.user_key == current_user.user_key)
    await session.execute(statement)
    await session.commit()
    return JSONResponse(content={"message": "success"}, status_code=204)


class WinGameReq(BaseModel):
    product_location: str
    get_product_time: str
    longitude: float
    latitude: float


@game_router.post("/start/{product_key}")
async def start_game(
    current_user: Annotated[User, Depends(get_current_active_user)],
    product_key: int,
    session: AsyncSession = Depends(get_session),
):
    """
    게임이 시작된다.
    """
    statement = select(Game).where(Game.product_key == product_key)
    result = await session.execute(statement)
    game = result.scalar_one_or_none()
    if not game:
        return JSONResponse(content={"message": "게임이 존재하지 않습니다."}, status_code=400)
    game.is_started = True
    session.add(game)
    await session.commit()


@game_router.post("/win/{product_key}")
async def win_game(
    current_user: Annotated[User, Depends(get_current_active_user)],
    req: WinGameReq,
    product_key: int,
    session: AsyncSession = Depends(get_session),
):
    """
    유저가 게임에서 승리한다.
    """
    statement = select(Game).where(Game.product_key == product_key)
    result = await session.execute(statement)
    game = result.scalar_one_or_none()
    if not game:
        return JSONResponse(content={"message": "게임이 존재하지 않습니다."}, status_code=400)
    # 게임에 참여하고 있지 않은 경우에는 에러를 리턴한다.
    statement = (
        select(UserGame)
        .where(UserGame.user_key == current_user.user_key)
        .where(UserGame.game_key == game.game_key)
    )
    result = await session.execute(statement)
    current_user_joined_game: UserGame = result.one()
    if len(current_user_joined_game) == 0:
        return JSONResponse(
            content={"message": "해당 유저는 게임에 참여하고 있지 않습니다."}, status_code=400
        )

    # 정보 업데이트
    current_user_joined_game.is_win = True
    current_user_joined_game.product_location = req.product_location
    current_user_joined_game.get_product_time = req.get_product_time
    current_user_joined_game.longitude = req.longitude
    current_user_joined_game.latitude = req.latitude

    session.add(current_user_joined_game)
    await session.commit()

    return JSONResponse(content={"message": "success"}, status_code=204)
