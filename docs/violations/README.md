# Violations

## `TC0xx` - Exception Classes


| Code              | Description                                                |
| ----------------- | ---------------------------------------------------------- |
| [TC002](TC002.md) | Create your own exception                                  |
| [TC003](TC003.md) | Avoid specifying long messages outside the exception class |

## `TC1xx` - General


| Code                                 | Description           |
| ------------------------------------ | --------------------- |
| [TC100](TC100.md) (**EXPERIMENTAL**) | Check to continue     |
| [TC101](TC101.md)                    | Too many `try` blocks |

## `TC2xx` - Except blocks


| Code              | Description                                         |
| ----------------- | --------------------------------------------------- |
| [TC200](TC200.md) | Use `raise Exception from`                          |
| [TC201](TC201.md) | Simply use `raise`                                  |
| [TC202](TC202.md) | Don't ignore a broad exception without even logging |

## `TC3xx` - Try blocks


| Code              | Description                       |
| ----------------- | --------------------------------- |
| [TC300](TC300.md) | Consider adding an `else` block   |
| [TC301](TC301.md) | Avoid direct raises in `try` body |
