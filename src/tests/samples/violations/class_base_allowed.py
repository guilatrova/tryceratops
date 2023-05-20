"""
Violation:

Forbid inherit from Exception if needed
"""


from typing import Any


class AllowedExc(Exception):
    pass


class AlsoAllowed(Exception):
    pass


class InvalidBase(Exception):  # Err
    pass


class MultiInvalidBase(ValueError, Exception):  # Err
    pass


class ThisIsFine(AllowedExc):
    pass


class ThisIsAlsoFine(AlsoAllowed):
    pass
