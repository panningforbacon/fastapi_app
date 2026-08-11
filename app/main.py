from fastapi import FastAPI

from app.__version__ import __version__
from app.config import Settings, get_settings
from app.lifespan import lifespan
from app.routers import health


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title="Hello API",
        version=__version__,
        lifespan=lifespan,
        description="A minimal FastAPI service.",
    )

    app.state.settings = settings

    @app.get("/")
    async def read_root() -> dict[str, str]:
        return {"message": "Hello world!"}

    app.include_router(health.router, tags=["ops"])

    return app
