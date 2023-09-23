from datetime import datetime

from sqlmodel import select

from database.models import Product
from src.products.dtos.dtos import GameType


class ProductRepository:
    def __init__(self, session):
        self.session = session

    async def get_product_detail(self, product_key: int):
        """
        상품 디테일 조회
        """
        statement = select(Product).where(Product.product_key == product_key)
        results = await self.session.exec(statement)
        product = results.first()
        return product

    async def get_products(self):
        """
        상품 목록 조회
        """
        statement = select(Product)
        results = await self.session.exec(statement)
        products = results.all()
        return products

    async def create_product(
        self,
        title: str,
        category_key: int,
        description: str,
        location: str,
        latitude: float,
        longitude: float,
        game_type: GameType,
        max_participants: int,
        user_key: int,
        valid_start_time: datetime,
        valid_end_time: datetime,
    ):
        product = Product(
            title=title,
            category_key=category_key,
            description=description,
            location=location,
            latitude=latitude,
            longitude=longitude,
            game_type=game_type,
            max_participants=max_participants,
            user_key=user_key,
            valid_start_time=valid_start_time,
            valid_end_time=valid_end_time,
        )
        self.session.add(product)
        await self.session.commit()
