from dataclasses import dataclass


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str


TOO_MANY_TRY = ("TC001", "Too many try blocks in your function")
RAISE_VANILLA_CLASS = ("TC002", "Create your own exception")
RAISE_VANILLA_ARGS = (
    "TC003",
    "Avoid specifying long messages outside the exception class",
)
