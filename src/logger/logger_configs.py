from loguru import logger

import sys
from pathlib import Path


def setup_logger():

    logger.remove()

    project_root = Path(__file__).parent.parent.resolve()
    log_dir = project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    logger.add(
        sys.stdout,
        colorize=True,
        level="DEBUG",
        enqueue=True,  # важно для асинхронных приложений
    )

    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="100 MB",
        retention="7 days",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        enqueue=True,
        serialize=True
    )

    return logger