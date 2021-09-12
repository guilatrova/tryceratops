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


def func():
    try:
        a = 1
    except Exception as error:  # already set, should reuse
        raise MyException()


def shouldnt_implement_handler_twice():
    try:
        a = 1
    except Exception:
        if a == b:
            raise MyException()
        else:
            raise MyException()


def longer_reraise():
    try:
        a = 1
    except Exception:
        # Multi-line!
        raise MyException(
            1,
            2,
            3,
            4,
        )
