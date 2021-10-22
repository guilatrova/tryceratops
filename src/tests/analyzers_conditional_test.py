from functools import partial

from tryceratops import analyzers
from tryceratops.violations import codes

from .analyzer_helpers import assert_violation, read_sample


def test_prefer_type_error():
    tree = read_sample("conditional_prefer_type_error")
    analyzer = analyzers.conditional.PreferTypeErrorAnalyzer()

    assert_type_error = partial(
        assert_violation, codes.PREFER_TYPE_ERROR[0], codes.PREFER_TYPE_ERROR[1]
    )

    violations = analyzer.check(tree, "filename")

    assert len(violations) == 31

    assert_type_error(12, 14, violations[0])
    assert_type_error(19, 14, violations[1])
    assert_type_error(30, 14, violations[2])
    assert_type_error(37, 14, violations[3])
    assert_type_error(44, 14, violations[4])
    assert_type_error(51, 14, violations[5])
    assert_type_error(58, 14, violations[6])
    assert_type_error(65, 14, violations[7])
    assert_type_error(72, 14, violations[8])
    assert_type_error(79, 14, violations[9])
    assert_type_error(86, 14, violations[10])
    assert_type_error(93, 14, violations[11])
    assert_type_error(100, 14, violations[12])
    assert_type_error(107, 14, violations[13])
    assert_type_error(114, 14, violations[14])
    assert_type_error(121, 14, violations[15])
    assert_type_error(128, 14, violations[16])
    assert_type_error(135, 14, violations[17])
    assert_type_error(142, 14, violations[18])
    assert_type_error(149, 14, violations[19])
    assert_type_error(156, 14, violations[20])
    assert_type_error(163, 14, violations[21])
    assert_type_error(170, 14, violations[22])
    assert_type_error(177, 14, violations[23])
    assert_type_error(184, 14, violations[24])
    assert_type_error(191, 14, violations[25])
    assert_type_error(198, 14, violations[26])
    assert_type_error(205, 14, violations[27])
    assert_type_error(212, 14, violations[28])
    assert_type_error(219, 14, violations[29])
    assert_type_error(226, 14, violations[30])
