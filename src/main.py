from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def api_app() -> FastAPI:
    from src.auth import routers
    # from src.user.routers import router as user_router

    api = FastAPI(
        title="API",
        docs_url="/docs",
        redoc_url="/redoc",
        version="0.1.0",
    )

    @api.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content=jsonable_encoder({"detail": exc.errors()}),
        )

    api.include_router(routers.router, prefix="/auth", tags=["auth"])

    return api


app = FastAPI(title="Investa platform", version="0.1.0", lifespan=lifespan)

app.mount("/api/v1", api_app())
