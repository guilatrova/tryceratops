import sys

from tryceratops.analyzers import Runner
from tryceratops.settings import ERROR_LOG_FILENAME
from tryceratops.violations import Violation


class COLORS:
    DESCR = "\033[91m"
    CODE = "\033[93m"

    ENDC = "\033[0m"


def wrap_color(msg: str, color: str):
    return f"{color}{msg}{COLORS.ENDC}"


def present_violation(violation: Violation):
    codestr = wrap_color(violation.code, COLORS.CODE)
    descstr = wrap_color(violation.description, COLORS.DESCR)
    location = f"{violation.filename}:{violation.line}:{violation.col}"

    return f"[{codestr}] {descstr} - {location}"


class CliInterface:
    def __init__(self, runner: Runner):
        self.runner = runner

    def _present_violations(self):
        for violation in self.runner.violations:
            print(present_violation(violation))

    def _present_status(self):
        print("Done processing! 🦖✨")
        print(f"Processed {self.runner.analyzed_files} files")
        print(f"Found {len(self.runner.violations)} violations")

        if self.runner.had_issues:
            print(
                f"Had {len(self.runner.runtime_errors)} unexpected issues "
                f"stored in {ERROR_LOG_FILENAME}"
            )

    def _exit(self):
        exit_code = 0

        if self.runner.had_issues:
            exit_code = 2
        elif self.runner.any_violation:
            exit_code = 1

        sys.exit(exit_code)

    def present_and_exit(self):
        self._present_violations()
        self._present_status()
        self._exit()
