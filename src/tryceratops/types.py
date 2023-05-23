import ast
import sys
import typing as t

if sys.version_info >= (3, 11):
    import typing as te
else:
    import typing_extensions as te

from tryceratops.settings import FileFilter

ParsedFileType = t.Tuple[str, ast.AST, FileFilter]
ParsedFilesType = t.Collection[ParsedFileType]


class PyprojectConfig(t.TypedDict):
    """
    Represents the expected pyproject config to be loaded
        exclude: a list of path patterns to be excluded e.g. [/tests, /fixtures]
        ignore: a list of violations to be completely ignored e.g. [TRY002, TRY300]
        experimental: whether to enable experimental analyzers
    """

    exclude: te.NotRequired[t.List[str]]
    ignore: te.NotRequired[t.List[str]]
    experimental: te.NotRequired[bool]
    autofix: te.NotRequired[bool]
    check_pickable: te.NotRequired[bool]
    allowed_base_exceptions: te.NotRequired[bool]
