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
        raise ex  # notc: TC202


def verbose_reraise_2():
    try:
        a = 1
    except Exception as ex:
        if a == 1:
            raise ex  # notc: TC202, TC200, TC201 I want to skip


def too_many_try():
    try:
        a = 1
    except Exception:
        raise

    try:  # notc:TC101 this is not a big deal
        b = 2
    except Exception:
        raise
