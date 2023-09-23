from datetime import datetime
from enum import IntEnum
from typing import Optional

from pydantic import BaseModel


class GameType(IntEnum):
    first_come_game = 0
    click_game = 1
    color_game = 2
    time_limit_game = 3


class CreateProductReq(BaseModel):
    title: str
    category_key: int
    description: str
    location: str
    latitude: float
    longitude: float
    game_type: GameType
    max_participants: int
    valid_start_time: datetime
    valid_end_time: datetime
    is_valid: Optional[bool] = True
