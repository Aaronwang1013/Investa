from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_view import inertia, view
from pydantic import ValidationError

from src.config import settings, vite


@asynccontextmanager
async def lifespan(app: FastAPI):
    # vite.jinja2_env_import(view.templates.env)
    inertia.share("version", settings.APP_VERSION)

    yield


def api_app() -> FastAPI:
    from src.auth import routers as auth_routers
    from src.user import routers as user_routers
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

    api.include_router(auth_routers.router, prefix="/auth", tags=["auth"])
    api.include_router(user_routers.router, prefix="/users", tags=["users"])
    return api


def web_app() -> FastAPI:
    from src.views import routers as view_routers

    web = FastAPI(title="Web")

    web.include_router(view_routers.router, prefix="", tags=["home"])

    return web


app = FastAPI(title="Investa platform", version="0.1.0", lifespan=lifespan)

app.mount("/api/v1", api_app())
app.mount("/", web_app())
