# crosszip

[![PyPI Version](https://img.shields.io/pypi/v/crosszip.svg)](https://pypi.org/project/crosszip/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

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

## Usage - main function

### Using Lists

```python
from crosszip import crosszip

def concat(a, b, c):
    return f"{a}-{b}-{c}"

list1 = [1, 2]
list2 = ['a', 'b']
list3 = [True, False]

result = crosszip(concat, list1, list2, list3)
print(result)
# Output: ['1-a-True', '1-a-False', '1-b-True', '1-b-False', '2-a-True', '2-a-False', '2-b-True', '2-b-False']
```

### Using Tuples

```python
def add(a, b):
    return a + b

result = crosszip(add, (1, 2), (10, 20))
print(result)
# Output: [11, 21, 12, 22]
```

### Using Sets and Generators

```python
def concat(a, b):
    return f"{a}{b}"

set1 = {1, 2}
gen = (x for x in ["x", "y"])

result = crosszip(concat, set1, gen)
print(result)
# Output: ['1x', '1y', '2x', '2y']
```

---

## Usage - pytest plugin

The `crosszip_parametrize` marker allows you to define parameter names and their corresponding values:

```python
import pytest
from crosszip import crosszip_parametrize

@crosszip_parametrize("a", [1, 2], "b", [3, 4])
def test_example(a, b):
    assert (a, b) in [(1, 3), (1, 4), (2, 3), (2, 4)]
```

---

## License

This project is licensed under the [MIT License](LICENSE.md).

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
