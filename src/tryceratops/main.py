import ast
from os import listdir
from os.path import isdir, isfile, join
from typing import Generator, Tuple


def is_python_file(filename: str):
    return isfile(filename) and filename.endswith(".py")


def parse_file(filename: str) -> ast.AST:
    with open(filename) as content:
        return ast.parse(content.read())


def find_files(dir: str) -> Generator[str, None, None]:
    files = listdir(dir)
    for entry in files:
        full_path = join(dir, entry)
        if isdir(full_path):
            yield from find_files(full_path)
        elif is_python_file(full_path):
            yield full_path


def parse_python_files_from_dir(dir: str) -> Generator[Tuple[str, ast.AST], None, None]:
    if is_python_file(dir):
        yield (dir, parse_file(dir))
    elif isdir(dir):
        for filename in find_files(dir):
            yield (filename, parse_file(filename))
