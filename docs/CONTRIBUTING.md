# Contributing

- [Contributing](#contributing)
  - [Setup](#setup)
  - [Testing](#testing)
  - [Linting](#linting)
  - [Conventional Commits](#conventional-commits)

## Setup

Install the dependency manager (if not already done):

```sh
pip3 install poetry
```

Install all dependencies, pre-commit hooks, and git config:

```sh
poetry install
pre-commit install
git config commit.template .gitmessage
```

and you should be ready to go!

```sh
❯ poetry run tryceratops --version
tryceratops, version 2.4.0
```

## Testing

You can either run:

```sh
❯ poetry run pytest
================================================ test session starts ================================================
platform darwin -- Python 3.9.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /Users/guilhermelatrova/guilatrova/tryceratops
collected 16 items

src/tests/analyzers_test.py .........                                                                         [ 56%]
src/tests/files_test.py .......                                                                               [100%]

================================================ 16 passed in 0.09s =================================================
```

or test it against some violation files we have in place:

```sh
❯ poetry run tryceratops src/tests/samples/violations/call_too_many_try.py
[TRY101] Too many try blocks in your function - src/tests/samples/violations/call_too_many_try.py:15:4
[TRY101] Too many try blocks in your function - src/tests/samples/violations/call_too_many_try.py:27:4
[TRY101] Too many try blocks in your function - src/tests/samples/violations/call_too_many_try.py:32:4
Done processing! 🦖✨
Processed 1 files
Found 3 violations
```

You can try it with flake8 if preferred:

```sh
❯ poetry run flake8 --select TRY src/tests/samples/violations/call_too_many_try.py
src/tests/samples/violations/call_too_many_try.py:15:5: TRY101 Too many try blocks in your function
src/tests/samples/violations/call_too_many_try.py:27:5: TRY101 Too many try blocks in your function
src/tests/samples/violations/call_too_many_try.py:32:5: TRY101 Too many try blocks in your function
```

## Linting

If you installed `pre-commit` it should ensure you're not commiting anything broken.

You can run `./bin/lint` to fix some issues for you.

## Conventional Commits

We automate the versioning and release process! It's only possible if we are consistent with the commit pattern and follow the conventional commits standards.

Refer to [Conventional Commits here](https://www.conventionalcommits.org/en/v1.0.0/) and if you're curious to understand how the publishing works [check here](https://python-semantic-release.readthedocs.io/en/latest/).
