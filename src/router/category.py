from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from database.connection import get_session
from database.models import Category

category_router = APIRouter(
    tags=["Category"],
)


@category_router.get("/list")
async def get_category_list(
    # current_user: Annotated[User, Depends(get_current_active_user)],
    session: AsyncSession = Depends(get_session),
):
    """
    카테고리 리스트 조회
    """
    statement = select(Category)
    results = await session.exec(statement)
    categories = results.all()
    return categories
