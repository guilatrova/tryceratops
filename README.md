<p align="center">
    <img src="https://raw.githubusercontent.com/guilatrova/tryceratops/main/img/logo.png">
</p>

<h2 align="center">Prevent Exception Handling AntiPatterns in Python</h2>

<p align="center">
  <a href="https://github.com/guilatrova/tryceratops/actions"><img alt="Actions Status" src="https://github.com/guilatrova/tryceratops/workflows/CI/badge.svg"></a>
  <a href="https://pypi.org/project/tryceratops/"><img alt="PyPI" src="https://img.shields.io/pypi/v/tryceratops"/></a>
  <img src="https://badgen.net/pypi/python/tryceratops" />
  <a href="https://github.com/relekang/python-semantic-release"><img alt="Semantic Release" src="https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg"></a>
  <a href="https://github.com/guilatrova/tryceratops/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/guilatrova/tryceratops"/></a>
  <a href="https://pepy.tech/project/tryceratops/"><img alt="Downloads" src="https://static.pepy.tech/personalized-badge/tryceratops?period=total&units=international_system&left_color=grey&right_color=blue&left_text=%F0%9F%A6%96%20Downloads"/></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>
  <a href="https://github.com/guilatrova/tryceratops"><img alt="try/except style: tryceratops" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black" /></a>
  <a href="https://twitter.com/intent/user?screen_name=guilatrova"><img alt="Follow guilatrova" src="https://img.shields.io/twitter/follow/guilatrova?style=social"/></a>
</p>

Inspired by [this blog post](https://blog.guilatrova.dev/handling-exceptions-in-python-like-a-pro/). I described [the building process of this tool here](https://blog.guilatrova.dev/project-tryceratops/).

> “For those who like dinosaurs 🦖 and clean try/except ✨ blocks.”

**Summary**
- [Installation and usage](#installation-and-usage)
  - [Installation](#installation)
  - [Usage](#usage)
  - [`flake8` Plugin](#flake8-plugin)
- [Violations](#violations)
  - [Autofix support](#autofix-support)
  - [Ignoring violations](#ignoring-violations)
  - [Configuration](#configuration)
- [Pre-commit](#pre-commit)
- [Show your style](#show-your-style)
- [Extra Resources](#extra-resources)
- [Contributing](#contributing)
- [Change log](#change-log)
- [License](#license)
- [Credits](#credits)

---

## Installation and usage

### Installation

```
pip install tryceratops
```

OR

```
poetry add -D tryceratops
```

### Usage

```
tryceratops [filename or dir...]
```

You can enable experimental analyzers by running:

```
tryceratops --experimental [filename or dir...]
```

You can ignore specific violations by using: `--ignore TRYXXX` repeatedly:

```
tryceratops --ignore TRY201 --ignore TRY202 [filename or dir...]
```

You can exclude dirs by using: `--exclude dir/path` repeatedly:

```
tryceratops --exclude tests --exclude .venv [filename or dir...]
```

You can also autofix some violations:

```
tryceratops --autofix [filename or dir...]
```

![example](https://raw.githubusercontent.com/guilatrova/tryceratops/main/img/tryceratops-example3.gif)

### [`flake8`](https://github.com/PyCQA/flake8) Plugin

🦖 Tryceratops is also a plugin for `flake8`, so you can:

```
❯ flake8 --select TRY src/tests/samples/violations/call_raise_vanilla.py
src/tests/samples/violations/call_raise_vanilla.py:13:9: TRY002 Create your own exception
src/tests/samples/violations/call_raise_vanilla.py:13:9: TRY003 Avoid specifying long messages outside the exception class
src/tests/samples/violations/call_raise_vanilla.py:21:9: TRY201 Simply use 'raise' without specifying exception object again
```

## Violations

All violations and its descriptions can be found in [docs](https://github.com/guilatrova/tryceratops/tree/main/docs/violations).

### Autofix support

So far, autofix only supports violations: [TRY200](docs/violations/TRY200.md), [TRY201](docs/violations/TRY201.md), and [TRY400](docs/violations/TRY400.md).

### Ignoring violations

If you want to ignore a violation in a specific file, you can either:

- Add a comment with `noqa` to the top of the file you want to ignore
- Add a comment with `noqa` to the line you want to ignore
- Add a comment with `noqa: CODE` to the line you want to ignore a specific violation

Example:

```py
def verbose_reraise_1():
    try:
        a = 1
    except Exception as ex:
        raise ex  # noqa: TRY202
```

### Configuration

You can set up a `pyproject.toml` file to set rules.
This is useful to avoid reusing the same CLI flags over and over again and helps to define the structure of your project.

Example:

```toml
[tool.tryceratops]
exclude = ["samples"]
ignore = ["TRY002", "TRY200", "TRY300"]
experimental = false
check_pickable = false
allowed_base_exceptions = ["MyAppBase"]
```

CLI flags always overwrite the config file.

## Pre-commit

If you wish to use pre-commit, add this:

```yaml
  - repo: https://github.com/guilatrova/tryceratops
    rev: v2.3.1
    hooks:
      - id: tryceratops
```

## Show your style

[![try/except style: tryceratops](https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black)](https://github.com/guilatrova/tryceratops)

Add this fancy badge to your project's `README.md`:

```md
[![try/except style: tryceratops](https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black)](https://github.com/guilatrova/tryceratops)
```

## Extra Resources

If you want to read more about:

- [How to structure exceptions in Python 🐍 🏗️ 💣](https://blog.guilatrova.dev/how-to-structure-exception-in-python-like-a-pro/)
- [How to log in Python 🐍🌴](https://blog.guilatrova.dev/how-to-log-in-python-like-a-pro/)
- [Book: Effective Python](https://amzn.to/3bEVHpG)

## Contributing

Thank you for considering making Tryceratops better for everyone!

Refer to [Contributing docs](docs/CONTRIBUTING.md).

## Change log

See [CHANGELOG](CHANGELOG.md).

## License

MIT

## Credits

Thanks to God for the inspiration 🙌 ☁️ ☀️

The [black](https://github.com/psf/black) project for insights.
