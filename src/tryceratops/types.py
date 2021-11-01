import ast
import sys
from typing import Collection, List, Tuple

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from tryceratops.filters import FileFilter

ParsedFileType = Tuple[str, ast.AST, FileFilter]
ParsedFilesType = Collection[ParsedFileType]


class PyprojectConfig(TypedDict):
    """
    Represents the expected pyproject config to be loaded
        exclude: a list of path patterns to be excluded e.g. [/tests, /fixtures]
        ignore: a list of violations to be completely ignored e.g. [TC002, TC300]
        experimental: whether to enable experimental analyzers
    """

    exclude: List[str]
    ignore: List[str]
    experimental: bool
    autofix: bool
