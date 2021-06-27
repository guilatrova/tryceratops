import ast
import os

from tryceratops.files.parser import parse_file
from tryceratops.filters.entities import IgnoreViolation


def get_full_path(filename: str):
    ref_dir = f"{os.path.dirname(__file__)}/samples/ignore_comments/"
    path = f"{ref_dir}{filename}.py"
    return path


def test_parse_ignore_line():
    filename = get_full_path("ignore_line")
    tree, filter = parse_file(filename)
    ignore_lines = filter.ignore_lines

    assert isinstance(tree, ast.AST)
    assert len(ignore_lines) == 3
    assert all([ignore.code is None for ignore in ignore_lines])

    first, second, third = ignore_lines
    assert first.line == 13
    assert second.line == 21
    assert third.line == 30


def test_parse_specific_code_line():
    filename = get_full_path("ignore_line_specific")
    tree, filter = parse_file(filename)
    ignore_lines = filter.ignore_lines

    assert isinstance(tree, ast.AST)
    assert len(ignore_lines) == 3

    first, second, third = ignore_lines
    assert first.line == 13
    assert first.code == ["TC202"]

    assert second.line == 21
    assert second.code == ["TC202", "TC200", "TC201"]

    assert third.line == 30
    assert third.code == ["TC001"]


def test_entity_ignores_all():
    ignore = IgnoreViolation(10)

    assert ignore.is_ignoring(10, "TC200") is True
    assert ignore.is_ignoring(10, "TC100") is True
    assert ignore.is_ignoring(10, "TC300") is True
    assert ignore.is_ignoring(10, "anything") is True

    assert ignore.is_ignoring(12, "TC200") is False
    assert ignore.is_ignoring(12, "TC100") is False
    assert ignore.is_ignoring(12, "TC300") is False
    assert ignore.is_ignoring(12, "anything") is False


def test_entity_ignores_specific():
    ignore = IgnoreViolation(10, ["TC200", "TC001"])

    assert ignore.is_ignoring(10, "TC200") is True
    assert ignore.is_ignoring(10, "TC001") is True
    assert ignore.is_ignoring(10, "TC100") is False
    assert ignore.is_ignoring(10, "TC300") is False
    assert ignore.is_ignoring(10, "anything") is False
