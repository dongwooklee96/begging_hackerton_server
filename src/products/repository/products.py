from datetime import datetime

from database.models import Product
from src.products.dtos.dtos import GameType


class ProductRepository:
    def __init__(self, session):
        self.session = session

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
