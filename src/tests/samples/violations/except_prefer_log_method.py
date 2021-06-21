"""
Violation:

Use '.exception' over '.error' inside except blocks
"""

import logging

logger = logging.getLogger(__name__)


def func():
    try:
        a = 1
    except Exception:
        logger.error("log message")
