"""
Violation:

Raising an exception and catching inside the same function is confusing
and may indicate that a inner function should be doing it instead
"""
import logging

logger = logging.getLogger(__name__)


class MyException(Exception):
    pass


def func():
    a = 1

    try:
        if a == 1:
            raise MyException()
    except MyException:
        logger.exception("reraise + catch in the same place is weird")
