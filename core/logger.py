"""
NOVARYN Logger
Centralized logging for the entire application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

from config.settings import LOG_DIR, LOG_FILE, LOG_LEVEL

# ----------------------------------------------------
# Ensure log directory exists
# ----------------------------------------------------

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

console = Console()

# ----------------------------------------------------
# Common formatter
# ----------------------------------------------------

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

formatter = logging.Formatter(
    LOG_FORMAT,
    datefmt=DATE_FORMAT
)

# ----------------------------------------------------
# File Handler
# ----------------------------------------------------

file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,      # 5 MB
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)

# ----------------------------------------------------
# Console Handler
# ----------------------------------------------------

console_handler = RichHandler(
    rich_tracebacks=True,
    show_path=False,
    markup=True
)

console_handler.setFormatter(
    logging.Formatter("%(message)s")
)

# ----------------------------------------------------
# Root Logger
# ----------------------------------------------------

root_logger = logging.getLogger("NOVARYN")

root_logger.setLevel(LOG_LEVEL)

if not root_logger.handlers:
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

root_logger.propagate = False

# ----------------------------------------------------
# Logger Factory
# ----------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Returns a child logger.

    Example:
        logger = get_logger("oracle_chamber")
        logger.info("Oracle initialized")
    """
    return root_logger.getChild(name)

# ----------------------------------------------------
# Startup Banner
# ----------------------------------------------------

logger = get_logger("startup")

logger.info("=" * 60)
logger.info("NOVARYN Logging Initialized")
logger.info(f"Log File : {LOG_FILE}")
logger.info(f"Log Level: {LOG_LEVEL}")
logger.info("=" * 60)