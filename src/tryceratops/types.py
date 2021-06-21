import ast
from typing import Iterable, Tuple

ParsedFileType = Tuple[str, ast.AST]
ParsedFilesType = Iterable[Tuple[str, ast.AST]]
