from functools import partial

from tryceratops import analyzers
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
