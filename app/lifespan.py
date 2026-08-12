import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.logging_config import configure_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    try:
        settings = get_settings()
        configure_logging(settings)

        logger.info(f"Logging level={logger.level}")
        logger.debug("Settings=" + settings.model_dump_json(indent=2))

        yield {}

    finally:
        # cleanup
        print("[lifespan] Cleaning up & closing.")
        pass
