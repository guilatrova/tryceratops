import logging.config

import click

from tryceratops.analyzers import analyze
from tryceratops.main import parse_python_files_from_dir
from tryceratops.settings import LOGGING_CONFIG


@click.command()
@click.argument("dir")
def entrypoint(dir: str):
    parsed_files = list(parse_python_files_from_dir(dir))
    violations = list(analyze(parsed_files))

    for violation in violations:
        print(str(violation))


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()
