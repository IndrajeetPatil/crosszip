# crosszip

[![PyPI Version](https://img.shields.io/pypi/v/crosszip.svg)](https://pypi.org/project/crosszip/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/crosszip.svg)](https://pypi.org/project/crosszip/)
[![Tests](https://github.com/IndrajeetPatil/crosszip/actions/workflows/tests.yml/badge.svg)](https://github.com/IndrajeetPatil/crosszip/actions)

`crosszip` is a Python utility that makes it easy to apply a function to all possible combinations of elements from multiple iterables.
It combines the power of the Cartesian product and functional programming into a single, intuitive tool.

---

## Installation

Install `crosszip` via pip:

```bash
pip install crosszip
```

---

## Key Features

- **Flexible Input**: Works with any iterables, including lists, tuples, sets, and generators.
- **Error Handling**: Detects and raises errors for invalid input types.
- **Simple API**: Minimalist, intuitive design for quick integration into your projects.

---

## Usage

### Basic Example

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

### Advanced Examples

#### Mathematical Computation with Tuples

```python
def add(a, b):
    return a + b

result = crosszip(add, (1, 2), (10, 20))
print(result)
# Output: [11, 21, 12, 22]
```

#### Using Sets and Generators

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
