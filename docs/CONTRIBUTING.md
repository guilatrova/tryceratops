# Contributing

- [Contributing](#contributing)
  - [Environment](#environment)
  - [Testing](#testing)
  - [Linting](#linting)
  - [Conventional Commits](#conventional-commits)

## Environment

Today we use `flit` to build and publish packages (We're considering migrating to Poetry soon).
[Read more here](https://github.com/guilatrova/tryceratops/issues/19) if curious.

Here's how to install Tryceratops:

```sh
pip install -r dev-requirements.txt

pre-commit install

flit install --sym
```

and you should be ready to go!

```sh
❯ tryceratops --version
tryceratops, version 0.2.5
```

## Testing

You can either run:

```sh
❯ pytest
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
❯ tryceratops src/tests/samples/violations/call_too_many_try.py
[TC101] Too many try blocks in your function - src/tests/samples/violations/call_too_many_try.py:15:4
[TC101] Too many try blocks in your function - src/tests/samples/violations/call_too_many_try.py:27:4
[TC101] Too many try blocks in your function - src/tests/samples/violations/call_too_many_try.py:32:4
Done processing! 🦖✨
Processed 1 files
Found 3 violations
```

You can try it with flake8 if preferred:

```sh
❯ flake8 --select TC src/tests/samples/violations/call_too_many_try.py
src/tests/samples/violations/call_too_many_try.py:15:5: TC101 Too many try blocks in your function
src/tests/samples/violations/call_too_many_try.py:27:5: TC101 Too many try blocks in your function
src/tests/samples/violations/call_too_many_try.py:32:5: TC101 Too many try blocks in your function
```

## Linting

If you installed `pre-commit` it should ensure you're not commiting anything broken.

You can run `./bin/lint` to fix some issues for you.

Please note `mypy` is broken, [we're going to solve it eventually](https://github.com/guilatrova/tryceratops/issues/17).

## Conventional Commits

We have plans to automate the versioning and release process and it's only possible if we follow the conventional commits standards. Otherwise, the versioning might be inconsistent later on.

Refer to [Conventional Commits here](https://www.conventionalcommits.org/en/v1.0.0/) and if you're curious to understand how the automation works (not implemented yet) [check it here](https://mestrak.com/blog/semantic-release-with-python-poetry-github-actions-20nn).
