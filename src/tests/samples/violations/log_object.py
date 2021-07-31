"""
Violation:

Use '.exception' over '.error' inside except blocks
"""

import logging

logger = logging.getLogger(__name__)


def func():
    try:
        a = 1
    except Exception as ex:
        logger.exception(f"log message {ex}")
        logger.exception("log message: " + ex)
        logger.exception("log message", ex)
