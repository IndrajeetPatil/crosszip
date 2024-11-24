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

## Usage

Example of using `crosszip`:

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

Example of using `pytest` marker `crosszip_parametrize`:

```python
import math
from crosszip_parametrize import crosszip_parametrize

@crosszip_parametrize(
    "base", [2, 10],
    "exponent", [-1, 0, 1],
)
def test_power_function(base, exponent):
    result = math.pow(base, exponent)
    assert result == base ** exponent
```

For more examples, check out the package documentation at:
https://indrajeetpatil.github.io/crosszip/

---

## License

This project is licensed under the [MIT License](LICENSE.md).
