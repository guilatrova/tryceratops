from os import listdir
from os.path import isdir, isfile, join
from typing import Generator, Iterable

from tryceratops.types import ParsedFileType

from .parser import parse_file


def is_python_file(filename: str):
    return isfile(filename) and filename.endswith(".py")


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
        parsed, filefilter = parse_file(dir)
        if parsed:
            yield (dir, parsed, filefilter)

    elif isdir(dir):
        for filename in find_files(dir):
            parsed, filefilter = parse_file(filename)
            if parsed:
                yield (filename, parsed, filefilter)


def parse_python_files(files: Iterable[str]) -> Generator[ParsedFileType, None, None]:
    for file in files:
        yield from parse_python_files_from_dir(file)
