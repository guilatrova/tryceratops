import logging
import toml
from dataclasses import dataclass
from os import listdir
from os.path import isdir, isfile, join
from pathlib import Path
from typing import Generator, Iterable, List, Optional, Sequence, Tuple

from tryceratops.types import ParsedFileType, PyprojectConfig

from .parser import parse_file

logger = logging.getLogger(__name__)


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


@dataclass
class FileParseFailed:
    filename: str
    reason: str
    exception: Exception


class FileDiscovery:
    def __init__(self):
        self.failures: List[FileParseFailed] = []

    @property
    def had_issues(self) -> bool:
        return len(self.failures) > 0

    def _parse_python_files_from_dir(self, dir: str) -> Generator[ParsedFileType, None, None]:
        files = []
        if is_python_file(dir):
            files.append(dir)
        elif isdir(dir):
            files = find_files(dir)

        for filename in files:
            try:
                parsed, filefilter = parse_file(filename)
            except Exception as ex:
                logger.exception(f"Failed to parse file {filename}, skipping it")
                self.failures.append(FileParseFailed(filename, str(ex), ex))
            else:
                if parsed:
                    yield (filename, parsed, filefilter)

    def parse_python_files(self, files: Iterable[str]) -> Generator[ParsedFileType, None, None]:
        for file in files:
            yield from self._parse_python_files_from_dir(file)


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
