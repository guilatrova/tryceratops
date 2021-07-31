"""
Violation:

Do not log exception object
"""

import logging

logger = logging.getLogger(__name__)


def func_fstr():
    try:
        ...
    except Exception as ex:
        logger.exception(f"log message {ex}")


def func_concat():
    try:
        ...
    except Exception as ex:
        logger.exception("log message: " + str(ex))


def func_comma():
    try:
        ...
    except Exception as ex:
        logger.exception("log message", ex)
