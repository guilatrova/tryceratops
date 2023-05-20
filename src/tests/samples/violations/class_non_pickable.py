"""
Violation:

Implement __reduce__ to enforce class is pickable.
"""


from typing import Any


class RandomClass:
    """This is not even an exception"""


class RegularException(Exception):
    pass


class AnotherOkException(Exception):
    def __init__(self, val1: str) -> None:
        super().__init__(val1)


class ManyArgsMissingReduce(Exception):
    def __init__(self, val1: str, val2: str) -> None:  # Requires pickable
        super().__init__(f"{val1} {val2}")


class CustomMissingReduce(Exception):
    def __init__(self, age: int) -> None:  # Requires pickable
        super().__init__(f"You're not old enough: {age}")


class ManyArgsWITHReduce(Exception):
    def __init__(self, val1: str, val2: str) -> None:
        self.val1, self.val2 = val1, val2
        super().__init__(f"{val1} {val2}")

    def __reduce__(self) -> str | tuple[Any, ...]:
        return (ManyArgsWITHReduce, (self.val1, self.val2))


class CustomWITHReduce(Exception):
    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"You're not old enough: {age}")

    def __reduce__(self) -> str | tuple[Any, ...]:
        return (CustomMissingReduce, (self.age,))


class ParentException(Exception):
    pass


class ChildrenExceptionMissingReduce(ParentException):
    def __init__(self, age: int) -> None:  # TODO: Should be a violation!
        self.age = age
        super().__init__(f"You're not old enough: {age}")
