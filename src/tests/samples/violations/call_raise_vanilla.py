"""
Violation:

Raising vanilla exception with custom message means it should be
customized.
"""


def func():
    a = 1
    if a == 1:
        raise Exception("Custom message")


def ignore():
    try:
        a = 1
    except Exception as ex:
        # This is another violation, but this specific analyzer shouldn't care
        raise ex
