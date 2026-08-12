from fastapi import FastAPI

from app.__version__ import __version__
from app.config import Settings, get_settings
from app.error_handlers import register_error_handlers
from app.lifespan import lifespan
from app.middleware import register_middleware
from app.routers import health, root


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title="Hello API",
        version=__version__,
        lifespan=lifespan,
        description="A minimal FastAPI service.",
    )

    app.state.settings = settings

    register_middleware(app)
    register_error_handlers(app)

    @app.get("/")
    async def read_root() -> dict[str, str]:
        return {"message": "Hello world!"}

    app.include_router(root.router)
    app.include_router(health.router, tags=["ops"])

    return app
