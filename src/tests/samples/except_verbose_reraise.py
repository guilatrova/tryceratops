"""
Violation:

Don't specify exception object again
"""

def func():
    try:
        a = 1
    except Exception as ex:
        raise ex

