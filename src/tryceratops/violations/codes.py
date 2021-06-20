# TC0xx
TOO_MANY_TRY = ("TC001", "Too many try blocks in your function")
RAISE_VANILLA_CLASS = ("TC002", "Create your own exception")
RAISE_VANILLA_ARGS = (
    "TC003",
    "Avoid specifying long messages outside the exception class",
)

# TC1xx
CHECK_TO_CONTINUE = (
    "TC100",
    "Don't check to continue, make callable '{}' raise a exception instead",
)

# TC2xx
RERAISE_NO_CAUSE = ("TC200", "Use 'raise from' to specify exception cause")
VERBOSE_RERAISE = (
    "TC201",
    "Simply use 'raise' without specifying exception object again",
)
