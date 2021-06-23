# TC0xx - Exceptions
TOO_MANY_TRY = ("TC001", "Too many try blocks in your function")
RAISE_VANILLA_CLASS = ("TC002", "Create your own exception")
RAISE_VANILLA_ARGS = (
    "TC003",
    "Avoid specifying long messages outside the exception class",
)

# TC1xx - General
CHECK_TO_CONTINUE = (
    "TC100",
    "Don't check to continue, make callable '{}' raise a exception instead",
)

# TC2xx - Except
RERAISE_NO_CAUSE = ("TC200", "Use 'raise from' to specify exception cause")
VERBOSE_RERAISE = (
    "TC201",
    "Simply use 'raise' without specifying exception object again",
)
IGNORING_EXCEPTION = ("TC202", "You're ignoring a broad exception without even logging")

# TC3xx - Try
CONSIDER_ELSE = ("TC300", "Consider moving this statement to an 'else' block")
