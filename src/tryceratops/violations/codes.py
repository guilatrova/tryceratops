# TRY0xx - Exceptions
RAISE_VANILLA_CLASS = ("TRY002", "Create your own exception")
RAISE_VANILLA_ARGS = (
    "TRY003",
    "Avoid specifying long messages outside the exception class",
)
PREFER_TYPE_ERROR = ("TRY004", "Prefer TypeError exception for invalid type")

# TRY1xx - General
CHECK_TO_CONTINUE = (
    "TRY100",
    "Don't check to continue, make callable '{}' raise a exception instead",
)
TOO_MANY_TRY = ("TRY101", "Too many try blocks in your function")

# TRY2xx - Except
RERAISE_NO_CAUSE = ("TRY200", "Use 'raise from' to specify exception cause")
VERBOSE_RERAISE = (
    "TRY201",
    "Simply use 'raise' without specifying exception object again",
)
IGNORING_EXCEPTION = ("TRY202", "You're ignoring a broad exception without even logging")
USELESS_TRY_EXCEPT = ("TRY203", "Useless try-except, remove it or handle the exception")

# TRY3xx - Try
CONSIDER_ELSE = ("TRY300", "Consider moving this statement to an 'else' block")
RAISE_WITHIN_TRY = ("TRY301", "Abstract raise to an inner function")

# TRY4xx - Logging
USE_LOGGING_EXCEPTION = ("TRY400", "Use logging '.exception' instead of '.error'")
VERBOSE_LOG_MESSAGE = ("TRY401", "Do not log exception object, give context instead")

CODE_CHOICES = {
    "TRY002",
    "TRY003",
    "TRY100",
    "TRY101",
    "TRY200",
    "TRY201",
    "TRY202",
    "TRY300",
    "TRY301",
    "TRY302",
    "TRY400",
    "TRY401",
}
