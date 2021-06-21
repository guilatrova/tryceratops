import logging.config

import click

import tryceratops
from tryceratops.analyzers import Runner
from tryceratops.interfaces import CliInterface
from tryceratops.main import parse_python_files_from_dir
from tryceratops.settings import LOGGING_CONFIG

runner = Runner()
interface = CliInterface(runner)


@click.command()
@click.argument("dir")
@click.version_option(tryceratops.__version__)
def entrypoint(dir: str):
    parsed_files = list(parse_python_files_from_dir(dir))
    interface.present_and_exit(parsed_files)


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()


if __name__ == "__main__":
    main()
