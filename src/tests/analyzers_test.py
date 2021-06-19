import ast
import os
from functools import partial

from tryceratops.analyzers import CallRaiseVanillaAnalyzer, CallTooManyAnalyzer
from tryceratops.violations import Violation, codes


def read_sample(filename: str) -> ast.AST:
    ref_dir = f"{os.path.dirname(__file__)}/samples/"
    path = f"{ref_dir}{filename}.py"

    with open(path) as sample:
        content = sample.read()
        loaded = ast.parse(content)
        return loaded


def assert_violation(code: str, msg: str, line: int, col: int, violation: Violation):
    assert violation.line == line
    assert violation.col == col
    assert violation.code == code
    assert violation.description == msg


def test_too_many_calls():
    tree = read_sample("call_too_many_try")
    analyzer = CallTooManyAnalyzer()
    expected_code, expected_msg = codes.TOO_MANY_TRY
    assert_too_many = partial(assert_violation, expected_code, expected_msg)

    violations = list(analyzer.check(tree))

    assert len(violations) == 3
    v2blocks, v3blocks_1, v3blocks_2 = violations

    assert_too_many(15, 4, v2blocks)
    assert_too_many(27, 4, v3blocks_1)
    assert_too_many(32, 4, v3blocks_2)


def test_raise_vanilla():
    tree = read_sample("call_raise_vanilla")
    analyzer = CallRaiseVanillaAnalyzer()

    assert_args = partial(
        assert_violation, codes.RAISE_VANILLA_ARGS[0], codes.RAISE_VANILLA_ARGS[1]
    )
    assert_class = partial(
        assert_violation, codes.RAISE_VANILLA_CLASS[0], codes.RAISE_VANILLA_CLASS[1]
    )

    violations = list(analyzer.check(tree))

    assert len(violations) == 2
    class_vio, args_vio = violations

    assert_class(12, 8, class_vio)
    assert_args(12, 8, args_vio)
