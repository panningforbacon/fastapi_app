import logging
from contextvars import ContextVar
from logging.config import dictConfig

from app.config import Settings

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


def configure_logging(settings: Settings) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"request_id": {"()": RequestIdFilter}},
            "formatters": {
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(request_id)s %(message)s",
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "json",
                    "filters": ["request_id"],
                },
            },
            "root": {"handlers": ["stdout"], "level": settings.log_level},
            "loggers": {
                "uvicorn.error": {"level": settings.log_level, "propagate": True, "handlers": []},
                "uvicorn.access": {"level": "INFO", "propagate": True, "handlers": []},
            },
        }
    )
