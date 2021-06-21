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
@click.option(
    "--experimental",
    is_flag=True,
    type=bool,
    default=False,
    show_default=True,
    help="Whether to enable experimental analyzers",
)
@click.version_option(tryceratops.__version__)
def entrypoint(dir: str, experimental: bool):
    parsed_files = list(parse_python_files_from_dir(dir))
    runner.analyze(parsed_files, experimental)
    interface.present_and_exit()


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()


if __name__ == "__main__":
    main()
