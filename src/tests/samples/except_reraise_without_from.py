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

