import logging

from fastapi import FastAPI

from app.__version__ import __version__
from app.config import Settings, get_settings
from app.error_handlers import register_error_handlers
from app.lifespan import lifespan
from app.logging_config import configure_logging
from app.middleware import register_middleware
from app.routers import health, root

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = get_settings()
    configure_logging(settings)

    app = FastAPI(
        title="Hello API",
        version=__version__,
        lifespan=lifespan,
        description="A minimal FastAPI service.",
    )

    app.state.settings = settings

    register_middleware(app)
    register_error_handlers(app)

    app.include_router(root.router)
    app.include_router(health.router)

    logger.debug(f"Logging level={logger.level}")
    logger.debug(f"Settings={settings.model_dump_json(indent=2)}")

    return app
