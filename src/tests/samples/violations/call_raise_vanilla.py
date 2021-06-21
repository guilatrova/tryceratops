"""
Violation:

Raising vanilla exception with custom message means it should be
customized.
"""


def func():
    a = 1
    if a == 1:
        raise Exception("Custom message")
