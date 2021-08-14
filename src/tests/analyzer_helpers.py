import ast
import os
from typing import Iterable

from tryceratops.violations import Violation


def read_sample(filename: str) -> ast.AST:
    ref_dir = f"{os.path.dirname(__file__)}/samples/violations/"
    path = f"{ref_dir}{filename}.py"

    with open(path) as sample:
        content = sample.read()
        loaded = ast.parse(content)
        return loaded


def read_sample_lines(filename: str) -> Iterable[str]:
    ref_dir = f"{os.path.dirname(__file__)}/samples/violations/"
    path = f"{ref_dir}{filename}.py"

    with open(path) as sample:
        return sample.readlines()


def assert_violation(code: str, msg: str, line: int, col: int, violation: Violation):
    assert violation.line == line
    assert violation.col == col
    assert violation.code == code
    assert violation.description == msg
