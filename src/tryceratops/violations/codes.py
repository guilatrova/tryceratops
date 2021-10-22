# TC0xx - Exceptions
RAISE_VANILLA_CLASS = ("TC002", "Create your own exception")
RAISE_VANILLA_ARGS = (
    "TC003",
    "Avoid specifying long messages outside the exception class",
)
PREFER_TYPE_ERROR = ("TC004", "Prefer TypeError exception for invalid type")

# TC1xx - General
CHECK_TO_CONTINUE = (
    "TC100",
    "Don't check to continue, make callable '{}' raise a exception instead",
)
TOO_MANY_TRY = ("TC101", "Too many try blocks in your function")

# TC2xx - Except
RERAISE_NO_CAUSE = ("TC200", "Use 'raise from' to specify exception cause")
VERBOSE_RERAISE = (
    "TC201",
    "Simply use 'raise' without specifying exception object again",
)
IGNORING_EXCEPTION = ("TC202", "You're ignoring a broad exception without even logging")

# TC3xx - Try
CONSIDER_ELSE = ("TC300", "Consider moving this statement to an 'else' block")
RAISE_WITHIN_TRY = ("TC301", "Abstract raise to an inner function")

# TC4xx - Logging
USE_LOGGING_EXCEPTION = ("TC400", "Use logging '.exception' instead of '.error'")
VERBOSE_LOG_MESSAGE = ("TC401", "Do not log exception object, give context instead")

CODE_CHOICES = {
    "TC002",
    "TC003",
    "TC100",
    "TC101",
    "TC200",
    "TC201",
    "TC202",
    "TC300",
    "TC301",
    "TC400",
    "TC401",
}
