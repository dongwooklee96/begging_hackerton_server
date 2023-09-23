from datetime import datetime
from typing import Optional

from sqlmodel import Field
from sqlmodel import SQLModel


# 공통 컬럼 모델
# ----------------------------------------------------
class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )


# ----------------------------------------------------


# 엔티티 테이블
# ----------------------------------------------------
class User(TimestampModel, table=True):
    """
    유저 테이블
    """

    __tablename__ = "user"

    user_key: int = Field(primary_key=True)
    id: int
    nick_name: Optional[str] = None
    profile_url: Optional[str] = None


class Category(TimestampModel, table=True):
    """
    카테고리 테이블
    """

    __tablename__ = "category"

    category: int = Field(primary_key=True)
    category_name: str


class Product(TimestampModel, table=True):
    """
    상품 테이블
    """

    __tablename__ = "product"

    product_key: int = Field(primary_key=True)
    title: str
    category_key: int
    description: str
    location: str
    latitude: float
    longitude: float
    game_type: int
    max_participants: int
    user_key: int
    valid_start_time: datetime
    valid_end_time: datetime
    is_valid: Optional[bool] = True


class Prize(TimestampModel, table=True):
    """
    업적 테이블
    """

    __tablename__ = "prize"

    prize_key: int = Field(primary_key=True)
    prize_name: str


class Game(TimestampModel, table=True):
    """
    게임 테이블
    """

    __tablename__ = "game"

    game_key: int = Field(primary_key=True)
    user_key: int
    product_key: int
    is_started: bool = Field(default=False)


class ClickGame(TimestampModel, table=True):
    """
    게임 (클릭) 테이블
    """

    __tablename__ = "click_game"
    click_game_key: int = Field(primary_key=True)
    game_key: int


class TimeLimitGame(TimestampModel, table=True):
    """
    게임 (시간 제한) 테이블
    """

    __tablename__ = "time_limit_game"
    time_limit_game_key: int = Field(primary_key=True)
    game_key: int


class ColorGame(TimestampModel, table=True):
    """
    게임 (틀린 색갈 찾기) 테이블
    """

    __tablename__ = "color_game"
    color_game_key: int = Field(primary_key=True)
    game_key: int


# ----------------------------------------------------
# 엔티티 관계 테이블
# ----------------------------------------------------
class PrizeUser(TimestampModel, table=True):
    """
    업적 - 유저 관계 테이블
    """

    __tablename__ = "prize_user"
    prize_user_key: int = Field(primary_key=True)
    prize_key: int
    user_key: int


class UserGame(TimestampModel, table=True):
    """
    유저 - 게임 테이블
    게임에 참여하고 있는 유저의 관계를 보여준다
    """

    __tablename__ = "user_game"
    user_game_key: int = Field(primary_key=True)
    game_key: int
    user_key: int
    product_location: str = Field(nullable=True)
    latitude: float = Field(nullable=True)
    longitude: float = Field(nullable=True)
    is_winner: bool = Field(nullable=True)
    get_product_time: datetime = Field(nullable=True)


class ProductGame(TimestampModel, table=True):
    """
    제품 - 게임 테이블
    게임과 연관된 상품을 나타내는 테이블
    """

    __tablename__ = "product_game"
    product_game_key: int = Field(primary_key=True)
    product_key: int
    game_key: int


# ----------------------------------------------------
