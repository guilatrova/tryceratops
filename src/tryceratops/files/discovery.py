from os import listdir
from os.path import isdir, isfile, join
from pathlib import Path
from typing import Generator, Iterable, Optional, Sequence, Tuple

import toml

from tryceratops.types import ParsedFileType, PyprojectConfig

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


def find_project_root(srcs: Sequence[str]) -> Path:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.
    """
    if not srcs:
        srcs = [str(Path.cwd().resolve())]

    path_srcs = [Path(Path.cwd(), src).resolve() for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory


def find_pyproject_toml(path_search_start: Tuple[str, ...]) -> Optional[str]:
    """Find the absolute filepath to a pyproject.toml if it exists"""
    path_project_root = find_project_root(path_search_start)
    path_pyproject_toml = path_project_root / "pyproject.toml"
    if path_pyproject_toml.is_file():
        return str(path_pyproject_toml)


def load_config(dir: Sequence[str]) -> Optional[PyprojectConfig]:
    toml_file = find_pyproject_toml(dir)

    if toml_file:
        config = toml.load(toml_file)
        return config.get("tool", {}).get("tryceratops", {})
