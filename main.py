from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.connection import create_schema
from src.router.auth import auth_router
from src.router.category import category_router
from src.router.game import game_router
from src.router.product import product_router
from src.router.user import user_router

app = FastAPI()
app.router.redirect_slashes = False

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth")
app.include_router(product_router, prefix="/api/v1/product")
app.include_router(category_router, prefix="/api/v1/category")
app.include_router(game_router, prefix="/api/v1/game")
app.include_router(user_router, prefix="/api/v1/user")


@app.on_event("startup")
async def startup_event():
    await create_schema()


@app.get("/ping")
def pong():
    return "pong"
