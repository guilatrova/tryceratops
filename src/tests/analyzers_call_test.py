from functools import partial

from tryceratops import analyzers
from tryceratops.violations import codes

from .analyzer_helpers import assert_violation, read_sample


def test_too_many_calls():
    tree = read_sample("call_too_many_try")
    analyzer = analyzers.call.CallTooManyAnalyzer()
    expected_code, expected_msg = codes.TOO_MANY_TRY
    assert_too_many = partial(assert_violation, expected_code, expected_msg)

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 3
    v2blocks, v3blocks_1, v3blocks_2 = violations

    assert_too_many(15, 4, v2blocks)
    assert_too_many(27, 4, v3blocks_1)
    assert_too_many(32, 4, v3blocks_2)


def test_raise_vanilla():
    tree = read_sample("call_raise_vanilla")
    analyzer = analyzers.call.CallRaiseVanillaAnalyzer()

    assert_vanilla = partial(
        assert_violation, codes.RAISE_VANILLA_CLASS[0], codes.RAISE_VANILLA_CLASS[1]
    )

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 2
    exc_violation, base_exc_violation = violations

    assert_vanilla(14, 8, exc_violation)
    assert_vanilla(34, 8, base_exc_violation)


def test_raise_long_args():
    tree = read_sample("call_raise_long_str")
    analyzer = analyzers.call.CallRaiseLongArgsAnalyzer()

    assert_args = partial(
        assert_violation, codes.RAISE_VANILLA_ARGS[0], codes.RAISE_VANILLA_ARGS[1]
    )

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 3
    first, second, third = violations

    assert_args(17, 8, first)
    assert_args(23, 8, second)
    assert_args(29, 8, third)


def test_check_continue():
    tree = read_sample("call_check_continue")
    analyzer = analyzers.call.CallAvoidCheckingToContinueAnalyzer()
    msg = codes.CHECK_TO_CONTINUE[1].format("another_func")

    assert_check = partial(assert_violation, codes.CHECK_TO_CONTINUE[0], msg)

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 2
    first, second = violations

    assert_check(20, 4, first)
    assert_check(24, 4, second)
