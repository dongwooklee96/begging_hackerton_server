from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from database.models import User
from src.auth.auth import get_current_active_user
from src.products.application.products import ProductService
from src.products.dtos.dtos import CreateProductReq
from src.products.repository.products import ProductRepository

product_router = APIRouter(
    tags=["Product"],
)


@product_router.post("/")
async def create_product(
    current_user: Annotated[User, Depends(get_current_active_user)],
    req: CreateProductReq,
    session: AsyncSession = Depends(get_session),
):
    """
    상품 생성
    """
    product_service = ProductService(
        product_repository=ProductRepository(session=session)
    )
    await product_service.create_product(
        title=req.title,
        category_key=req.category_key,
        description=req.description,
        location=req.location,
        latitude=req.latitude,
        longitude=req.longitude,
        game_type=req.game_type,
        max_participants=req.max_participants,
        user_key=current_user.user_key,
        valid_start_time=req.valid_start_time,
        valid_end_time=req.valid_end_time,
    )


@product_router.put("/")
def update_product(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    상품 수정
    """
    print(current_user)
    return "pong"


@product_router.delete("/")
def delete_product(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    상품 삭제
    """
    print(current_user)
    return "pong"


@product_router.get("/list")
def get_products(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    상품 목록 조회
    """
    print(current_user)
    return "pong"


@product_router.get("/")
def get_product_detail(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    상품 상세 조회
    """
    print(current_user)
    return "pong"
