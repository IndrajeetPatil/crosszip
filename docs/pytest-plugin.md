## pytest-plugin: crosszip parametrization

Registering the crosszip marker for pytest is simple. Just add the following to your `pytest.ini` file:

```
[pytest]
markers =
    crosszip_parametrize: "mark test function for crosszip parametrization"
```

### Usage

The `crosszip_parametrize` marker allows you to define parameter names and their corresponding values:

```python
import pytest
from crosszip import crosszip_parametrize

@crosszip_parametrize("a", [1, 2], "b", [3, 4])
def test_example(a, b):
    assert (a, b) in [(1, 3), (1, 4), (2, 3), (2, 4)]
```
