import re
from abc import ABC, abstractmethod
from typing import List, Tuple

from tryceratops.violations import Violation, codes


class BaseFixer(ABC):
    violation_code: Tuple[str, str]
    fixes_made = 0

    def _filter_violations_in_scope(self, violations: List[Violation]) -> List[Violation]:
        scope_code, _ = self.violation_code
        relevant = [vio for vio in violations if vio.code == scope_code]
        return relevant

    @abstractmethod
    def _perform_fix(self, violation: Violation):
        pass

    def fix(self, violations: List[Violation]):
        relevant_violations = self._filter_violations_in_scope(violations)

        for violation in relevant_violations:
            self._perform_fix(violation)
            self.fixes_made += 1


class VerboseReraiseFixer(BaseFixer):
    violation_code = codes.VERBOSE_RERAISE

    def _perform_fix(self, violation: Violation):
        with open(violation.filename, "r+") as file:
            all_lines = file.readlines()

            guilty_line = all_lines[violation.line - 1]
            new_line = re.sub(r"raise.*", "raise", guilty_line)
            all_lines[violation.line - 1] = new_line

            file.seek(0)
            file.writelines(all_lines)
            file.truncate()
