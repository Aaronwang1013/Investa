from contextlib import asynccontextmanager
from fastapi import FastAPI




@asynccontextmanager
async def lifespan(app: FastAPI):
    yield   


# def api_app() -> FastAPI:
#     from src.Trade.router import firstrade_router
