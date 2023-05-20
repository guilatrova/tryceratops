from tryceratops.violations import Violation


class FixerException(Exception):
    pass


class FixerFixException(FixerException):
    def __init__(self, violation: Violation, filename: str) -> None:
        self.violation = violation
        self.filename = filename
        super().__init__(f"Attempt to fix violation {violation} on file {filename} failed")
