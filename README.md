# crosszip <img src="docs/assets/logo.png" align="right" width="240" />

[![PyPI Version](https://img.shields.io/pypi/v/crosszip.svg)](https://pypi.org/project/crosszip/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

`crosszip` is a Python utility that makes it easy to apply a function to all possible combinations of elements from multiple iterables.
It combines the power of the Cartesian product and functional programming into a single, intuitive tool.

Additionally, `@pytest.mark.crosszip_parametrize` is a `pytest` marker that simplifies running tests with all possible combinations of parameter values.
This is particularly useful for testing functions or components across multiple dimensions of input parameters.

## Installation

Install `crosszip` via pip:

```bash
pip install crosszip
```

To use the `crosszip_parametrize` marker for `pytest`, add the following line to `tests/conftest.py`:

```python
pytest_plugins = ["crosszip.plugin"]
```

Check that the marker was successfully loaded by running `pytest --markers`;
you should see `@pytest.mark.crosszip_parametrize(*args)` in the list.

## Usage

Example of using `crosszip`:

```python
# Label Generation for Machine Learning

from crosszip import crosszip

def create_label(category, subcategory, version):
    return f"{category}_{subcategory}_v{version}"

categories = ["cat", "dog"]
subcategories = ["small", "large"]
versions = ["1.0", "2.0"]

labels = crosszip(create_label, categories, subcategories, versions)
print(labels)
# Output: ['cat_small_v1.0', 'cat_small_v2.0', 'cat_large_v1.0', 'cat_large_v2.0', 'dog_small_v1.0', 'dog_small_v2.0', 'dog_large_v1.0', 'dog_large_v2.0']
```

Example of using `pytest` marker `crosszip_parametrize`:

```python
# Testing Power Function

import math
import crosszip

@pytest.mark.crosszip_parametrize(
    "base", [2, 10],
    "exponent", [-1, 0, 1],
)
def test_power_function(base, exponent):
    result = math.pow(base, exponent)
    assert result == base ** exponent
```

For more examples, check out the package documentation at:
<https://indrajeetpatil.github.io/crosszip/>

## Key Features

- **Flexible Input**: Works with any iterables, including lists, tuples, sets, and generators.
- **pytest Plugin**: Provides a `crosszip_parametrize` marker for running tests with multiple parameter values.
- **Simple API**: Minimalist, intuitive design for quick integration into your projects.

## License

This project is licensed under the MIT License.

## Acknowledgements

Hex sticker font is `Rubik`, and the image is taken from icon made by Freepik and available at flaticon.com.
