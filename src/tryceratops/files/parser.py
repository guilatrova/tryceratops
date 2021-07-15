import ast
import re
import tokenize
from io import TextIOWrapper
from typing import Generator, Iterable, Optional, Tuple

from tryceratops.filters import FileFilter, IgnoreViolation

IGNORE_TRYCERATOPS_TOKEN = "notc"
IGNORE_TOKEN_PATT = r"notc(: ?((TC\d{3},? ?)+))?"


def _build_ignore_line(match: re.Match, location: Tuple[int, int]) -> IgnoreViolation:
    lineno, _ = location
    if match.group(2) is not None:
        codes = [raw.strip() for raw in match.group(2).split(",")]
        return IgnoreViolation(lineno, codes)

    return IgnoreViolation(lineno)


def parse_ignore_tokens(
    tokens: Iterable[tokenize.TokenInfo],
) -> Generator[IgnoreViolation, None, None]:
    for token in tokens:
        toktype, tokval, start, *_ = token
        if toktype == tokenize.COMMENT:
            if match := re.search(IGNORE_TOKEN_PATT, tokval):
                yield _build_ignore_line(match, start)


def parse_ignore_comments_from_file(
    content: TextIOWrapper,
) -> Generator[IgnoreViolation, None, None]:
    tokens = tokenize.generate_tokens(content.readline)
    yield from parse_ignore_tokens(tokens)


def parse_tree(content: TextIOWrapper) -> Optional[ast.AST]:
    try:
        return ast.parse(content.read())
    except Exception:
        return None


def parse_file(filename: str) -> Optional[Tuple[ast.AST, FileFilter]]:
    with open(filename, "r") as content:
        tree = parse_tree(content)
        if tree:
            content.seek(0)
            ignore_lines = list(parse_ignore_comments_from_file(content))
            return tree, FileFilter(ignore_lines)

        return None
