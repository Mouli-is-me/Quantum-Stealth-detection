"""
AEGIS-X Structured Logging Module
Provides standardized logging instances for debugging and production tracking.
"""

import logging
import sys
from src.config import LOGGING_FORMAT, LOGGING_DATE_FORMAT


def get_aegis_logger(name: str = "AEGIS-X", level: int = logging.INFO) -> logging.Logger:
    """
    Returns a configured Python logger instance with standardized formatting.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
