from dataclasses import dataclass


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str
