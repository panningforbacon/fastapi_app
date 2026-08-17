import copy
import logging
from contextvars import ContextVar
from logging.config import dictConfig

from app.config import Settings

logger = logging.getLogger(__name__)

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True


class ColorConsoleFormatter(logging.Formatter):
    RESET = "\033[0m"

    LEVELNAME_COLORS = {
        "DEBUG": "\033[36m",  # cyan
        "INFO": "\033[32m",  # green
        "WARNING": "\033[33m",  # yellow
        "ERROR": "\033[31m",  # red
        "CRITICAL": "\033[1;37;41m",  # bold white on red
    }

    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style="%",
        validate=True,
        *,
        defaults=None,
        level_width=0,
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)
        self.level_width = level_width

    def format(self, record):
        return super().format(self.with_colored_level(record))

    def with_colored_level(self, record):
        """Return a shallow copy of *record* whose levelname carries color."""
        colored = copy.copy(record)
        colored.levelname = self.colorize_level(record.levelname)
        return colored

    def colorize_level(self, levelname):
        padded = f"{levelname:<{self.level_width}}" if self.level_width else levelname
        color = self.LEVELNAME_COLORS.get(levelname)
        if color is None:
            return padded
        return f"{color}{padded}{self.RESET}"


def configure_logging(settings: Settings) -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"request_id": {"()": RequestIdFilter}},
            "formatters": {
                "console": {
                    "()": "app.logging_config.ColorConsoleFormatter",
                    "format": "%(levelname)s %(name)s %(request_id)s: %(message)s",
                    "level_width": 8,
                },
                "json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(asctime)s %(levelname)s %(name)s %(request_id)s %(message)s",
                },
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                    "filters": ["request_id"],
                },
            },
            "root": {"handlers": ["stdout"], "level": settings.log_level},
            "loggers": {
                "uvicorn": {"level": settings.log_level, "propagate": True, "handlers": []},
                "uvicorn.error": {"level": settings.log_level, "propagate": True, "handlers": []},
                "uvicorn.access": {"level": "INFO", "propagate": True, "handlers": []},
            },
        }
    )
