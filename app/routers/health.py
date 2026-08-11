from fastapi import APIRouter

from app.__version__ import __version__

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "pass",
        "version": __version__,
    }
