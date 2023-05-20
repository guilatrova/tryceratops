from functools import partial

from tryceratops import analyzers
from tryceratops.settings import GlobalSettings
from tryceratops.violations import codes

from .analyzer_helpers import assert_violation, read_sample


def test_non_pickable_error():
    tree = read_sample("class_non_pickable")
    analyzer = analyzers.classdefs.NonPickableAnalyzer()

    assert_non_pickable = partial(
        assert_violation, codes.NON_PICKABLE_CLASS[0], codes.NON_PICKABLE_CLASS[1]
    )

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 2

    assert_non_pickable(24, 0, violations[0])
    assert_non_pickable(29, 0, violations[1])


def test_inherit_from_allowed_exceptions():
    tree = read_sample("class_base_allowed")
    allowed_base_exceptions = {"AllowedExc", "AlsoAllowed"}
    analyzer = analyzers.classdefs.InheritFromBaseAnalyzer(
        GlobalSettings(
            include_experimental=False,
            exclude_dirs=[],
            ignore_violations=[],
            allowed_base_exceptions=allowed_base_exceptions,
        )
    )

    asset_non_inherit = partial(assert_violation, codes.ALLOWED_BASE_EXCEPTION[0])
    msg_base = codes.ALLOWED_BASE_EXCEPTION[1]
    allowed_msg = ", ".join(allowed_base_exceptions)

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 2

    asset_non_inherit(msg_base.format("InvalidBase", allowed_msg), 19, 0, violations[0])
    asset_non_inherit(msg_base.format("MultiInvalidBase", allowed_msg), 23, 0, violations[1])


def test_inherit_from_allowed_exceptions_undefined():
    tree = read_sample("class_base_allowed")
    analyzer = analyzers.classdefs.InheritFromBaseAnalyzer(
        GlobalSettings(
            include_experimental=False,
            exclude_dirs=[],
            ignore_violations=[],
            allowed_base_exceptions=set(),
        )
    )

    violations = analyzer.check(tree, "filename")
    assert len(violations) == 0
