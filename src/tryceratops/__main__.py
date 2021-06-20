import logging.config

import click

from tryceratops.analyzers import Runner
from tryceratops.main import parse_python_files_from_dir
from tryceratops.settings import ERROR_LOG_FILENAME, LOGGING_CONFIG

runner = Runner()


def print_finished_status():
    print("Done processing! 🦖✨")
    print(f"Processed {runner.analyzed_files} files")
    print(f"Found {len(runner.violations)} violations")

    if runner.had_issues:
        print(
            f"Had {len(runner.runtime_errors)} unexpected issues "
            f"stored in {ERROR_LOG_FILENAME}"
        )


@click.command()
@click.argument("dir")
def entrypoint(dir: str):
    parsed_files = list(parse_python_files_from_dir(dir))
    violations = list(runner.analyze(parsed_files))

    for violation in violations:
        print(str(violation))

    print_finished_status()


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()
