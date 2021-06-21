"""
Violation:

Don't use bare except
"""


def func():
    try:
        a = 1
    except:
        raise
