"""
Violation:

Constantly checking for non None values may indicate your parent function
should be raising an exception instead of returning
"""


class MyException(Exception):
    pass


def another_func():
    return None  # should raise instead


def func():
    try:
        a = another_func()
        if not a:
            return

        b = another_func()
        if not b:
            return
    except Exception:
        raise
