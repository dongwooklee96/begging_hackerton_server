from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel


class User(SQLModel, table=True):
    __tablename__ = "user"

    user_key: int = Field(primary_key=True)
    email: str = Field()
    nickname: str = Field()
    deleted: bool = Field()
    created_at: datetime = Field()
    updated_at: datetime = Field()
