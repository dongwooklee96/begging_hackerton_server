from datetime import datetime

from src.products.dtos.dtos import GameType
from src.products.repository.products import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.repository = product_repository

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
        await self.repository.create_product(
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
