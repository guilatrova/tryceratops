import logging
import os
import sys
from enum import IntEnum

from rich import print

from tryceratops.files.discovery import FileDiscovery
from tryceratops.runners import Runner
from tryceratops.settings import ERROR_LOG_FILENAME
from tryceratops.violations import Violation


class ExitCodes(IntEnum):
    SUCCESS = 0
    LINT_BROKEN = 1
    UNPROCESSED_FILE = 2
    RUNTIME_ISSUES = 100


def present_violation(violation: Violation) -> str:
    codestr = violation.code
    descstr = violation.description
    location = f"{violation.filename}:{violation.line}:{violation.col}"

    return f"[[yellow]{codestr}[/yellow]] [red]{descstr}[/red] - {location}"


class CliInterface:
    def __init__(self, runner: Runner, discovery: FileDiscovery) -> None:
        self.runner = runner
        self.discovery = discovery

    def _present_violations(self) -> None:
        for violation in self.runner.violations:
            print(present_violation(violation))

    def _present_status(self) -> None:
        print("Done processing!")

        if self.runner.analyzed_files:
            print(f"Processed {self.runner.analyzed_files} files")

            if self.runner.violations:
                print(f"Found {len(self.runner.violations)} violations")
            else:
                print("[bold]Everything clean![/bold]")
        else:
            print("Nothing to check!")

        if self.runner.fixed_violations:
            print(f"Fixed {self.runner.fixed_violations} violations")

        if self.discovery.had_issues:
            print(f"[bold red]Failed to process {len(self.discovery.failures)} files[/bold red]")

        if self.runner.excluded_files:
            print(f"Skipped {self.runner.excluded_files} files")

        if self.runner.had_issues:
            print(
                f"Had {len(self.runner.runtime_errors)} unexpected issues "
                f"stored in {ERROR_LOG_FILENAME}"
            )

    def _exit(self) -> None:
        exit_code = ExitCodes.SUCCESS

        if self.runner.had_issues:
            exit_code = ExitCodes.RUNTIME_ISSUES
        elif self.discovery.had_issues:
            exit_code = ExitCodes.UNPROCESSED_FILE
        elif self.runner.any_violation:
            exit_code = ExitCodes.LINT_BROKEN

        sys.exit(exit_code)

    def _delete_empty_logs(self) -> None:
        cwd = os.getcwd()
        log_file_path = f"{cwd}/{ERROR_LOG_FILENAME}"
        is_log_empty = os.path.getsize(log_file_path) == 0

        if is_log_empty:
            os.remove(log_file_path)

    def present_and_exit(self) -> None:
        logging.shutdown()
        self._present_violations()
        self._present_status()
        self._delete_empty_logs()
        self._exit()
