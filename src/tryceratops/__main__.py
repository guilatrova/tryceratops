import logging.config

import click

import tryceratops
from tryceratops.analyzers import Runner
from tryceratops.interfaces import CliInterface
from tryceratops.main import parse_python_files
from tryceratops.settings import LOGGING_CONFIG

runner = Runner()
interface = CliInterface(runner)

EXPERIMENTAL_FLAG_OPTION = dict(is_flag=True, help="Whether to enable experimental analyzers.")


@click.command()
@click.argument("dir", nargs=-1)
@click.option("--experimental", **EXPERIMENTAL_FLAG_OPTION)
@click.version_option(tryceratops.__version__)
def entrypoint(dir: str, experimental: bool):
    parsed_files = list(parse_python_files(dir))
    runner.analyze(parsed_files, experimental)
    interface.present_and_exit()


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()


if __name__ == "__main__":
    main()
