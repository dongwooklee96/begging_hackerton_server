import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from database.config import db_config

config_name = os.getenv("ENV", "dev")
DATABASE_URL = db_config[config_name].SQLALCHEMY_DATABASE_URI

# Set the pool_size and max_overflow according to your requirements
pool_size = 40
max_overflow = 0

engine = AsyncEngine(
    create_engine(
        DATABASE_URL,
        echo=True,
        future=True,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )
)

async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def create_schema():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
