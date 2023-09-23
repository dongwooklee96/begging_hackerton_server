from fastapi import FastAPI

from src.router.auth import auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/v1/auth")


@app.get("/ping")
def pong():
    return "pong"
