import logging

logger = logging.getLogger(__name__)


def func():
    try:
        a = 1
    except Exception:
        logger.error("I'm using 'error', but should be using 'exception'")
