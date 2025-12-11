import os
import sys

from loguru import logger

from conf import setting


def configure_logging() -> None:
    """Configure global Loguru logger.

    This sets a single stdout sink with a level based on settings.DEBUG.
    """

    logger.remove()

    level = "DEBUG" if setting.DEBUG else "INFO"

    os.makedirs("logs", exist_ok=True)

    logger.add(
        sys.stdout,
        level=level,
        backtrace=True,
        diagnose=setting.DEBUG,
        enqueue=True,
    )

    logger.add(
        "logs/info.log",
        level="INFO",
        rotation="10 MB",
        retention="7 days",
        enqueue=True,
    )

    logger.add(
        "logs/error.log",
        level="ERROR",
        rotation="10 MB",
        retention="7 days",
        enqueue=True,
    )
