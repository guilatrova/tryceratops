import logging.config

import click

from tryceratops.settings import LOGGING_CONFIG


@click.command()
@click.argument("dir")
def entrypoint(dir: str):
    print(f"I got your {dir}")


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()
