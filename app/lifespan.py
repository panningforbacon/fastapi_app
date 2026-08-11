from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    try:
        print("[lifespan] Starting up & initializing.")

        settings = get_settings()
        print(settings.model_dump_json(indent=2))

        # configure_logging(settings)

        print("[lifespan] Yielding app resources (attached to `request.state`)")
        yield {}

    finally:
        # cleanup
        print("[lifespan] Cleaning up & closing.")
        pass
