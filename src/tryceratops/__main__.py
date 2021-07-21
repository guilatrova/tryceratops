import click
import logging.config
from typing import Tuple

import tryceratops
from tryceratops.analyzers import Runner
from tryceratops.files import FileDiscovery, load_config
from tryceratops.filters import GlobalFilter
from tryceratops.interfaces import CliInterface
from tryceratops.settings import LOGGING_CONFIG
from tryceratops.violations import CODE_CHOICES

runner = Runner()
discovery = FileDiscovery()
interface = CliInterface(runner, discovery)
logger = logging.getLogger("tryceratops")


EXPERIMENTAL_FLAG_OPTION = dict(is_flag=True, help="Whether to enable experimental analyzers.")
IGNORE_OPTION = dict(
    multiple=True,
    help="A violation to be ignored. e.g. -i TC200 -i TC201",
    type=click.Choice(CODE_CHOICES),
)
EXCLUDE_OPTION = dict(multiple=True, help="A dir to be excluded. e.g. -x tests/ -x fixtures/")
VERBOSE_OPTION = dict(is_flag=True, help="Will print more logging messages.")


@click.command()
@click.argument("dir", nargs=-1)
@click.option("--experimental", **EXPERIMENTAL_FLAG_OPTION)
@click.option("-i", "--ignore", **IGNORE_OPTION)
@click.option("-x", "--exclude", **EXCLUDE_OPTION)
@click.option("-v", "--verbose", **VERBOSE_OPTION)
@click.version_option(tryceratops.__version__)
def entrypoint(
    dir: Tuple[str],
    experimental: bool,
    ignore: Tuple[str, ...],
    exclude: Tuple[str, ...],
    verbose: bool,
):
    pyproj_config = load_config(dir)
    if pyproj_config:
        global_filter = GlobalFilter.create_from_config(pyproj_config)
        global_filter.overwrite_from_cli(experimental, ignore, exclude)
    else:
        global_filter = GlobalFilter(experimental, ignore, exclude)

    if verbose:
        logger = logging.getLogger("tryceratops")
        logger.setLevel(logging.DEBUG)

    parsed_files = list(discovery.parse_python_files(dir))
    runner.analyze(parsed_files, global_filter)

    interface.present_and_exit()


def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint(prog_name="tryceratops")


if __name__ == "__main__":
    main()
