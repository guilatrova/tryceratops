class MyException(Exception):
    pass


def verbose_reraise_1():
    try:
        a = 1
    except MyException:
        raise
    except (NotImplementedError, ValueError) as ex:
        raise
    except Exception as ex:
        raise ex  # notc


def verbose_reraise_2():
    try:
        a = 1
    except Exception as ex:
        if a == 1:
            raise ex  # notc


def too_many_try():
    try:
        a = 1
    except Exception:
        raise

    try:  # notc
        b = 2
    except Exception:
        raise
