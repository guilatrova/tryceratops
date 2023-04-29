from functools import partial

from tryceratops import analyzers
from tryceratops.violations import codes

from .analyzer_helpers import assert_violation, read_sample


def test_consider_else():
    tree = read_sample("try_consider_else")
    analyzer = analyzers.try_block.TryConsiderElseAnalyzer()
    code, msg = codes.CONSIDER_ELSE

    assert_consider = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 1
    violation = violations[0]

    assert_consider(20, 8, violation)


def test_finally_dont_consider_else():
    tree = read_sample("try_finally_dont_consider_else")
    analyzer = analyzers.try_block.TryConsiderElseAnalyzer()
    code, msg = codes.CONSIDER_ELSE

    assert_consider = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 1
    violation = violations[0]

    assert_consider(30, 8, violation)


def test_try_inner_raise():
    tree = read_sample("try_inner_raise")
    analyzer = analyzers.try_block.TryShouldntRaiseAnalyzer()
    code, msg = codes.RAISE_WITHIN_TRY

    assert_inner_raise = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 2
    violation = violations[0]

    assert_inner_raise(21, 12, violation)
