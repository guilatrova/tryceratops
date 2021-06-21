import ast
from os import listdir
from os.path import isdir, isfile, join
from typing import Generator, Iterable, Optional

from .types import ParsedFileType


def is_python_file(filename: str):
    return isfile(filename) and filename.endswith(".py")


def parse_file(filename: str) -> Optional[ast.AST]:
    with open(filename) as content:
        try:
            return ast.parse(content.read())
        except Exception:
            return None


def find_files(dir: str) -> Generator[str, None, None]:
    files = listdir(dir)
    for entry in files:
        full_path = join(dir, entry)
        if isdir(full_path):
            yield from find_files(full_path)
        elif is_python_file(full_path):
            yield full_path


def parse_python_files_from_dir(dir: str) -> Generator[ParsedFileType, None, None]:
    if is_python_file(dir):
        parsed = parse_file(dir)
        if parsed:
            yield (dir, parsed)

    elif isdir(dir):
        for filename in find_files(dir):
            parsed = parse_file(filename)
            if parsed:
                yield (filename, parsed)


def parse_python_files(files: Iterable[str]) -> Generator[ParsedFileType, None, None]:
    for file in files:
        yield from parse_python_files_from_dir(file)
