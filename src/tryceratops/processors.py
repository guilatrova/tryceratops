from typing import Tuple


class Processor:
    """
    Represents either an Analyzer or Fixer
    """

    EXPERIMENTAL = False
    violation_code: Tuple[str, str]
