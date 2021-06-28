import ast
from typing import Iterable, Tuple

from tryceratops.filters import FileFilter

ParsedFileType = Tuple[str, ast.AST, FileFilter]
ParsedFilesType = Iterable[ParsedFileType]
