"""
Violation:

Raising vanilla exception with custom message means it should be
customized.
"""
from somewhere import exceptions


class CustomException(Exception):
    pass


def func():
    a = 1
    if a == 1:
        raise CustomException("Long message")
    elif a == 2:
        raise CustomException("Short")  # This is acceptable
    elif a == 3:
        raise CustomException("its_code_not_message")  # This is acceptable
    elif a == 4:
        raise CustomException(f"long message with f-string {a}")
    elif a == 5:
        raise CustomException(f"code_{a}")
    elif a == 6:
        raise CustomException(f"code_{' ' + str(a)}")  # TODO: This should not be acceptable!
    elif a == 7:
        raise CustomException("long message number %s", a)
    elif a == 8:
        raise CustomException("code_message_number_%s", a)  # This is acceptable


def ignore():
    try:
        a = 1
    except Exception as ex:
        # This is another violation, but this specific analyzer shouldn't care
        raise ex


def anotherfunc():
    a = 1
    if a == 1:
        # TODO: Handle this scenario later, it's a violation
        raise exceptions.CustomException("Another except")
