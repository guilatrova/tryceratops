import ast
import os

from tryceratops.files.parser import parse_file


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
