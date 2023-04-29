"""
Violation:

Sometimes you just want `try` and `finally` (without `except`), which can't be used
with `else`.
"""
import logging

logger = logging.getLogger(__name__)


class MyException(Exception):
    pass


def fine():
    try:
        a = 1
        b = process()
        return b

    finally:
        logger.info("ok() is fine")



def bad():
    try:
        a = 1
        b = process()
        return b

    except Exception:
        logger.exception("You can add else here")

    finally:
        logger.info("except + finally = still issue")

