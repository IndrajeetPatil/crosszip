# Introduction

`crosszip` is a Python utility that makes it easy to apply a function to all possible combinations of elements from multiple iterables.
It combines the power of the Cartesian product and functional programming into a single, intuitive tool.

Additionally, `crosszip_parametrize` Pytest plugin is a decorator that simplifies running tests with all possible combinations of parameter values.
This is particularly useful for testing functions or components across multiple dimensions of input parameters.

---

## Installation

Install `crosszip` via pip:

```bash
pip install crosszip
```

Registering the crosszip marker for pytest is simple. Just add the following to your `pytest.ini` file:

```
[pytest]
markers =
    crosszip_parametrize: "mark test function for crosszip parametrization"
```

---

## Key Features

- **Flexible Input**: Works with any iterables, including lists, tuples, sets, and generators.
- **pytest Plugin**: Supports parametrization of tests using `crosszip`.
- **Simple API**: Minimalist, intuitive design for quick integration into your projects.

---

## License

This project is licensed under the MIT License.

---

## Links

- **PyPI**: [https://pypi.org/project/crosszip/](https://pypi.org/project/crosszip/)
- **Repository**: [https://github.com/IndrajeetPatil/crosszip](https://github.com/IndrajeetPatil/crosszip)
- **Documentation**: [Coming Soon]

---

## Acknowledgments

Inspired by Python's functional programming capabilities and itertools' powerful utilities.

---

Start crosszipping your iterables today! 🚀
