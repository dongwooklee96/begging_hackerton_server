from typing import Annotated

from fastapi import Depends, FastAPI

from database.connection import create_schema
from database.models import User
from src.auth.auth import (
    get_current_active_user,
)
from src.router.auth import auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1/auth")


@app.on_event("startup")
async def startup_event():
    await create_schema()


@app.get("/ping")
def pong():
    return "pong"


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]
