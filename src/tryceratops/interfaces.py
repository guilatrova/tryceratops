import sys

from tryceratops.analyzers import Runner
from tryceratops.settings import ERROR_LOG_FILENAME
from tryceratops.types import ParsedFilesType


class CliInterface:
    def __init__(self, runner: Runner):
        self.runner = runner

    def _present_violations(self, files: ParsedFilesType):
        violations = self.runner.analyze(files)

        for violation in violations:
            print(str(violation))

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

    def present_and_exit(self, files: ParsedFilesType):
        self._present_violations(files)
        self._present_status()
        self._exit()
