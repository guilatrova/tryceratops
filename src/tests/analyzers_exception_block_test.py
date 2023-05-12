import ast
from functools import partial

from tryceratops import analyzers
from tryceratops.violations import codes

from .analyzer_helpers import assert_violation, read_sample


def test_reraise_no_cause():
    tree = read_sample("except_reraise_no_cause")
    analyzer = analyzers.exception_block.ExceptReraiseWithoutCauseAnalyzer()
    code, msg = codes.RERAISE_NO_CAUSE

    assert_no_cause = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 1
    single = violations[0]

    assert_no_cause(16, 8, single)
    assert single.exception_name is None
    assert isinstance(single.except_node, ast.ExceptHandler)


def test_verbose_reraise():
    tree = read_sample("except_verbose_reraise")
    analyzer = analyzers.exception_block.ExceptVerboseReraiseAnalyzer()
    code, msg = codes.VERBOSE_RERAISE

    assert_verbose = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 2
    first, second = violations

    assert_verbose(20, 8, first)
    assert first.exception_name == "ex"
    assert_verbose(28, 12, second)
    assert second.exception_name == "ex"


def test_broad_pass():
    tree = read_sample("except_pass")
    analyzer = analyzers.exception_block.ExceptBroadPassAnalyzer()
    code, msg = codes.IGNORING_EXCEPTION

    assert_broad = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 3
    first, second, third = violations

    assert_broad(18, 8, first)
    assert_broad(27, 8, second)
    assert_broad(35, 12, third)


def test_useless_except():
    tree = read_sample("try_useless_except")

    analyzer = analyzers.exception_block.UselessTryExceptAnalyzer()
    code, msg = codes.USELESS_TRY_EXCEPT

    violations = analyzer.check(tree, "filename")
    assert_useless_except = partial(assert_violation, code, msg)

    assert len(violations) == 7
    assert_useless_except(22, 4, violations[0])
    assert_useless_except(54, 4, violations[1])
    assert_useless_except(62, 4, violations[2])
    assert_useless_except(70, 4, violations[3])
    assert_useless_except(78, 4, violations[4])
    assert_useless_except(88, 4, violations[5])
    assert_useless_except(153, 4, violations[6])


def test_log_error():
    tree = read_sample("log_error")
    analyzer = analyzers.exception_block.LogErrorAnalyzer()
    code, msg = codes.USE_LOGGING_EXCEPTION

    assert_log_error = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 1
    violation = violations[0]

    assert_log_error(15, 8, violation)


def test_log_object():
    tree = read_sample("log_object")
    analyzer = analyzers.exception_block.LogObjectAnalyzer()
    code, msg = codes.VERBOSE_LOG_MESSAGE

    assert_log_error = partial(assert_violation, code, msg)

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 3
    fstr, concat, comma = violations

    assert_log_error(16, 40, fstr)
    assert_log_error(23, 47, concat)
    assert_log_error(30, 40, comma)
