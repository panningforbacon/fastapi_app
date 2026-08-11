from fastapi import FastAPI

from __version__ import __version__

app = FastAPI(
    title="Hello API",
    description="A minimal FastAPI service.",
    version=__version__,
)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {
        "message": "Hello world!",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "pass",
        "version": __version__,
    }
