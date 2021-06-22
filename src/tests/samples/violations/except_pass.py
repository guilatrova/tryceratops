"""
Violation:

Except with pass
"""


class MyException(Exception):
    pass


def somefunc():
    try:
        a = 1
    except MyException:
        pass  # This is specific, so it should be fine
    except Exception:
        pass  # This is broad, that's weird


def someotherfunc():
    try:
        a = 1
    except MyException:
        ...  # This is specific, so it should be fine
    except Exception:
        ...  # This is broad, that's weird


class SomeClass:
    def some_method(self):
        try:
            a = 1
        except (MyException, Exception):
            pass  # This is broad, that's weird
