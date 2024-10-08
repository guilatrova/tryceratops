"""
Violation:

Raising vanilla exception with custom message means it should be
customized.
"""

from somewhere import exceptions


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


def anotherfunc():
    a = 1
    if a == 1:
        raise exceptions.Exception("Another except")  # That's fine


def anotherfunc():
    a = 1
    if a == 1:
        raise BaseException("Customer message - also an issue")
