"""
Violation:

Capturing an exception just to raise it again has no effect in runtime,
and is considered a bad practice.

It's recommended to either log the error, change the behavior on capture,
or just remove the try-except block.

"""
import logging

logger = logging.getLogger(__name__)


class MyException(Exception):
    pass


def func_blanket():
    # ERROR
    try:
        ...
    except:
        raise


def func_blanket_custom():
    # OK - raises other
    try:
        ...
    except:
        raise MyException


def func_blanket_custom_e():
    # OK - raises other
    try:
        ...
    except Exception as e:
        raise MyException


def func_blanket_custom_from_e():
    # OK - raises other
    try:
        ...
    except Exception as e:
        raise MyException from e


def func_blanket_as_e_reraise():
    # ERROR
    try:
        ...
    except Exception as e:
        raise e


def func_blanket_exception():
    # ERROR
    try:
        ...
    except Exception:
        raise


def func_specific_exception():
    # ERROR
    try:
        ...
    except MyException:
        raise


def func_custom_then_blanket():
    # ERROR - all are useless
    try:
        ...
    except MyException:
        raise
    except:
        raise


def func_three_useless():
    # ERROR - all are useless
    try:
        ...
    except MyException:
        raise
    except Exception:
        raise
    except:
        raise


def func_blanket_then_code():
    # OK - more than just a `raise` handler
    try:
        ...
    except:
        ...
        raise


def func_only_second_useless():
    # OK - more than just a `raise` (1st handler)
    try:
        ...
    except MyException:
        ...
    except:
        raise


def func_only_first_useless():
    # OK - more than just a `raise` (2nd handler)
    try:
        ...
    except MyException:
        raise
    except:
        ...
        raise


def func_multiple_second_and_third_useless():
    # OK - more than just a `raise` (1st handler)
    try:
        ...
    except MyException:
        ...
        raise
    except Exception:
        raise
    except:
        raise


def func_except_finally_vaild():
    # OK - not useless
    try:
        ...
    except:
        ...
    finally:
        ...


def func_except_finally_useless():
    # ERROR - useless
    try:
        ...
    except:
        raise
    finally:
        ...


def func_single_finally():
    try:
        ...
    finally:
        ...
