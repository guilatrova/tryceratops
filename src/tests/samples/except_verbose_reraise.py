"""
Violation:

Don't specify exception object again
"""


class MyException(Exception):
    pass


def func():
    try:
        a = 1
    except MyException:
        raise  # This is fine
    except (NotImplementedError, ValueError) as ex:
        raise  # This is fine
    except Exception as ex:
        raise ex  # This is verbose


def func():
    try:
        a = 1
    except Exception as ex:
        if a == 1:
            raise ex  # This is verbose
