# Pyodide Integration Demo

This page demonstrates interactive Python code execution using Pyodide.

## Simple Example

Try running this simple Python code:

```python
# @pyodide
# Simple calculation
result = 2 + 2
print(f"2 + 2 = {result}")
```

## Using crosszip

Here's an example using the `crosszip` package:

```python
# @pyodide
from crosszip import crosszip

def create_label(category, subcategory):
    return f"{category}_{subcategory}"

categories = ["cat", "dog"]
subcategories = ["small", "large"]

labels = crosszip(create_label, categories, subcategories)
print("Generated labels:")
for label in labels:
    print(f"  - {label}")
```

## Using pytest

Example with pytest (imported from crosszip):

```python
# @pyodide
import pytest
from crosszip import crosszip

# Test the crosszip function
def test_basic_crosszip():
    def add(a, b):
        return a + b
    
    result = crosszip(add, [1, 2], [10, 20])
    expected = [11, 21, 12, 22]
    assert result == expected
    print("✓ Test passed!")

# Run the test
test_basic_crosszip()
```

## Interactive Math

Try modifying and running this code:

```python
# @pyodide
import math

# Calculate fibonacci numbers
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Print first 10 fibonacci numbers
print("First 10 Fibonacci numbers:")
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

## Notes

- **First run**: The first time you click "Run", Pyodide needs to download (~8MB). This may take a few seconds.
- **Package loading**: Packages like `crosszip` and `pytest` are installed on the first run.
- **Browser execution**: All code runs in your browser - no server required!
- **Editable**: You can modify the code directly in the browser and re-run it.

## Performance Considerations

- Initial load time: 5-10 seconds for Pyodide + packages
- Subsequent runs: Near-instant
- Memory: Uses browser memory (typically 50-100MB)
- Limitations: Heavy computational tasks may be slow

## Comparison with Current Solution

### Current (mkdocs-run-code)
- ✅ Fast initial load
- ❌ Requires server-side execution
- ❌ Not truly interactive
- ✅ Can handle heavy computations

### Pyodide
- ❌ Slower initial load
- ✅ No server required
- ✅ Fully interactive
- ❌ Limited by browser resources
- ✅ Can install packages
- ✅ Works offline after initial load
