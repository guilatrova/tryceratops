<p align="center">
    <img src="https://raw.githubusercontent.com/guilatrova/tryceratops/main/img/logo.png">
</p>

<h2 align="center">Manage your exceptions in Python like a PRO</h2>

<p align="center">
  <a href="https://pypi.org/project/tryceratops/">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/tryceratops">
  </a>
  <a href="https://github.com/psf/black">
    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  </a>
  <a href="https://pepy.tech/project/tryceratops/">
    <img alt="Downloads" src="https://static.pepy.tech/personalized-badge/tryceratops?period=total&units=international_system&left_color=grey&right_color=blue&left_text=%F0%9F%A6%96%20Downloads">
  </a>

</p>

Currently in BETA (and very flaky).
Inspired by [this blog post](https://blog.guilatrova.dev/handling-exceptions-in-python-like-a-pro/).

> “For those who like dinosaurs 🦖 and clean try/except ✨ blocks.”

---

## Installation and usage

### Installation

```
pip install tryceratops
```

### Usage

```
tryceratops [filename or dir]
```

You can enable experimental analyzers by running:

```
tryceratops --experimental [filename or dir]
```

![example](https://raw.githubusercontent.com/guilatrova/tryceratops/main/img/tryceratops-example.gif)

## Violations

All violations and its descriptions can be found in [docs](https://github.com/guilatrova/tryceratops/tree/main/docs/violations).

## Pre-commit

If you wish to use pre-commit, add this:

```yaml
  - repo: https://github.com/guilatrova/tryceratops
    rev: v0.1.3
    hooks:
      - id: tryceratops
```

## License

MIT

## Credits

Thanks to God for the inspiration 🙌 ☁️ ☀️

Logo icon was made by [https://www.freepik.com](Freepik)
