"""
Violation:

Too many try/except blocks.
Keep it short to 1 per function.
"""


def func():
    try:
        a = 1
    except Exception:
        raise

    try:
        b = 2
    except Exception:
        raise


def func_two():
    try:
        a = 1
    except Exception:
        raise

    try:
        b = 2
    except Exception:
        raise

    try:
        c = 3
    except Exception:
        raise
