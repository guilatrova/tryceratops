from dataclasses import dataclass


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str


TOO_MANY_TRY = ("TC001", "Too many try blocks in your function")
