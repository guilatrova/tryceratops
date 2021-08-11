import re
from abc import ABC, abstractmethod
from typing import List, Tuple

from tryceratops.violations import Violation, codes


class BaseFixer(ABC):
    violation_code: Tuple[str, str]

    @classmethod
    def _filter_violations_in_scope(cls, violations: List[Violation]) -> List[Violation]:
        scope_code, _ = cls.violation_code
        relevant = [vio for vio in violations if vio.code == scope_code]
        return relevant

    @classmethod
    @abstractmethod
    def _perform_fix(cls, violation: Violation):
        pass

    @classmethod
    def fix(cls, violations: List[Violation]):
        relevant_violations = cls._filter_violations_in_scope(violations)
        for violation in relevant_violations:
            cls._perform_fix(violation)


class VerboseReraiseFixer(BaseFixer):
    violation_code = codes.VERBOSE_RERAISE

    @classmethod
    def _perform_fix(cls, violation: Violation):
        with open(violation.filename, "r+") as file:
            all_lines = file.readlines()

            guilty_line = all_lines[violation.line - 1]
            new_line = re.sub(r"raise.*", "raise", guilty_line)
            all_lines[violation.line - 1] = new_line

            file.seek(0)
            file.writelines(all_lines)
            file.truncate()
