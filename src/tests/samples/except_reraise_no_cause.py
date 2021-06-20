"""
Violation:

Reraise without using 'from'
"""


class MyException(Exception):
    pass


def func():
    try:
        a = 1
    except Exception:
        raise MyException()


def good():
    try:
        a = 1
    except Exception:
        raise  # Just reraising don't need 'from'
