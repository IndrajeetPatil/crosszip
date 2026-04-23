---
tags:
  - advanced
  - memory
  - performance
  - testing
  - parametrize
---

# Advanced Usage

This guide covers three practical scenarios that the basic examples leave open:

1. Testing a validation function against all combinations of input types and edge cases
2. Handling memory efficiency when working with large iterables
3. Managing test explosion when the Cartesian product grows too large

---

## Testing a Validation Function Across Input Types and Edge Cases

`@pytest.mark.crosszip_parametrize` is well-suited for exhaustively testing a function
against a grid of input types and edge cases. The marker uses alternating
`"param_name", [values]` pairs, and the full Cartesian product becomes the test matrix.

### The validation function under test

```python
def validate_input(value):
    """Accept only non-empty strings and positive numbers."""
    if not isinstance(value, (int, float, str)):
        raise TypeError(f"Unsupported type: {type(value).__name__}")
    if isinstance(value, str) and len(value) == 0:
        raise ValueError("String must not be empty")
    if isinstance(value, (int, float)) and value <= 0:
        raise ValueError("Number must be positive")
    return True
```

### Happy-path combinations

The following test generates `len([int, str, float]) × len([1, "hello", 3.14])` = **9 test cases**,
one for each combination of type and a known-valid value:

```python
import pytest


@pytest.mark.crosszip_parametrize(
    "input_type",
    [int, str, float],
    "valid_value",
    [1, "hello", 3.14],
)
def test_validate_input_happy_path(input_type, valid_value):
    result = validate_input(input_type(valid_value))
    assert result is True
```

### Edge-case combinations with expected failures

Stack `@pytest.mark.xfail` above `@pytest.mark.crosszip_parametrize` to mark
all generated test cases as expected failures. The two markers compose correctly
because `crosszip_parametrize` runs through pytest's `metafunc.parametrize` hook
and `xfail` is applied at the test-item level:

```python
import pytest


@pytest.mark.xfail(raises=(TypeError, ValueError), strict=True)
@pytest.mark.crosszip_parametrize(
    "input_type",
    [int, str, float],
    "edge_case",
    [None, "", 0],
)
def test_validate_input_edge_cases(input_type, edge_case):
    validate_input(edge_case)
```

`strict=True` means any test case that unexpectedly *passes* is itself reported
as a failure — useful for catching regressions where validation logic becomes
too permissive.

### Per-combination assertions with `pytest.raises`

When you need different assertions per combination, pre-compute the expected
exception and pass it as an additional parameter:

```python
import pytest


@pytest.mark.crosszip_parametrize(
    "bad_value",
    [None, "", 0, -1],
    "expected_exc",
    [TypeError, ValueError],
)
def test_validate_input_error_types(bad_value, expected_exc):
    with pytest.raises((TypeError, ValueError)):
        validate_input(bad_value)
```

!!! tip
    Use `pytest.raises` when you want to assert the *specific* exception type
    per combination. Use `@pytest.mark.xfail` when the entire matrix is expected
    to raise and you want a compact, readable declaration.

---

## Memory Efficiency and Large Iterables

### How crosszip allocates memory

`crosszip` is implemented as:

```python
list(itertools.starmap(func, itertools.product(*iterables)))
```

Two materialization points occur:

1. `itertools.product` buffers all input iterables into tuples in memory.
2. The outer `list()` call holds every return value of `func` simultaneously.

The total number of combinations follows the formula:

```
total_combinations = N₁ × N₂ × … × Nₖ
```

You can estimate this before calling `crosszip`:

```python
import math

sizes = [100, 50, 20, 10]
total = math.prod(sizes)
print(f"Total combinations: {total:,}")  # 1,000,000
```

!!! warning "Exponential growth"
    With 5 iterables of 100 elements each, `crosszip` must hold
    10,000,000,000 result objects in memory simultaneously.
    For large inputs, use a lazy approach instead.

### The lazy workaround: `itertools.product` as a generator

Since `crosszip` always returns a `list`, the only way to process combinations
one at a time — without loading all results — is to use `itertools.product`
directly in a generator function:

```python
import itertools


def process_lazily(func, *iterables):
    """Generator version of crosszip — yields one result at a time."""
    for combo in itertools.product(*iterables):
        yield func(*combo)


# Consume without materializing the full result list
large_a = range(1_000)
large_b = range(1_000)

for result in process_lazily(lambda a, b: a + b, large_a, large_b):
    # Each result is produced and can be discarded before the next is computed.
    pass
```

!!! note
    `itertools.product` still buffers the *input* iterables into tuples
    internally, so generator inputs are exhausted on the first call.
    Only the *output* stream is lazy.

### Chunk processing

For pipelines that need batches rather than individual results — writing to
disk, sending over a network, etc.:

```python
import itertools


def chunked_crosszip(func, chunk_size, *iterables):
    """Process combinations in fixed-size chunks."""
    combo_iter = itertools.product(*iterables)
    while True:
        chunk = list(itertools.islice(combo_iter, chunk_size))
        if not chunk:
            break
        yield [func(*combo) for combo in chunk]


# Process 1 000 combinations at a time
for batch in chunked_crosszip(str, 1_000, range(500), range(500)):
    # Flush batch to disk before fetching the next one
    pass
```

### Guard pattern: fail fast on oversized inputs

Add a pre-flight check using `math.prod` to raise a clear error before
`crosszip` silently consumes all available memory:

```python
import math
from crosszip import crosszip


def safe_crosszip(func, *iterables, limit: int = 10_000):
    """Call crosszip only if combination count is within the limit."""
    # Convert to lists so we can measure length without exhausting generators
    lists = [list(it) for it in iterables]
    total = math.prod(len(lst) for lst in lists)
    if total > limit:
        raise ValueError(
            f"Combination count {total:,} exceeds limit {limit:,}. "
            "Reduce input sizes or use a lazy approach."
        )
    return crosszip(func, *lists)
```

---

## Managing Test Explosion

### Understanding combinatorial growth

The number of test cases grows as the product of all value-list lengths:

| Parameters | Values each | Test cases |
|:----------:|:-----------:|:----------:|
| 2          | 3           | 9          |
| 3          | 4           | 64         |
| 4          | 5           | 625        |
| 5          | 10          | 100,000    |
| 6          | 10          | 1,000,000  |

A realistic example that quietly produces 64 test cases:

```python
import pytest


@pytest.mark.crosszip_parametrize(
    "protocol",
    ["http", "https", "ftp", "ssh"],
    "method",
    ["GET", "POST", "PUT", "DELETE"],
    "auth_type",
    ["none", "basic", "token", "oauth"],
)
def test_api_client(protocol, method, auth_type): ...  # 4 × 4 × 4 = 64 test cases
```

### Strategy 1: Pre-filter combinations

`crosszip_parametrize` always generates the full Cartesian product. When only a
subset of combinations is meaningful, pre-filter with `itertools.product` and
pass the result to the standard `pytest.mark.parametrize`:

```python
import itertools
import pytest

protocols = ["http", "https", "ftp", "ssh"]
methods = ["GET", "POST", "PUT", "DELETE"]

# Only test secure protocols with write methods
meaningful_combos = [
    (proto, method)
    for proto, method in itertools.product(protocols, methods)
    if proto == "https" or method == "GET"
]
# Reduces 4 × 4 = 16 → 7 combinations


@pytest.mark.parametrize("protocol,method", meaningful_combos)
def test_secure_api(protocol, method): ...
```

### Strategy 2: Use `-k` for focused runs during development

pytest's `-k` flag matches test IDs by substring, letting you run a slice of
the generated matrix without changing any code:

```bash
# Run only the https combinations
pytest -k "https"

# Run only POST combinations
pytest -k "POST"

# Narrow further with boolean operators
pytest -k "https and POST"
```

### Strategy 3: Random sampling with a fixed seed

Statistical coverage without full enumeration — and deterministic enough for CI:

```python
import itertools
import random
import pytest

protocols = ["http", "https", "ftp", "ssh"]
methods = ["GET", "POST", "PUT", "DELETE"]
all_combos = list(itertools.product(protocols, methods))

SEED = 42  # fix the seed so CI runs are reproducible
sampled = random.Random(SEED).sample(all_combos, k=min(5, len(all_combos)))


@pytest.mark.parametrize("protocol,method", sampled)
def test_api_sample(protocol, method): ...
```

### Strategy 4: Split into focused test classes

Divide a large parameter space into smaller, purpose-scoped classes so each
runs only the combinations relevant to its concern:

```python
import pytest


class TestCoreProtocols:
    @pytest.mark.crosszip_parametrize(
        "method",
        ["GET", "POST"],
        "auth",
        ["none", "basic"],
    )
    def test_http_methods(self, method, auth): ...  # 2 × 2 = 4 tests


class TestSecureProtocols:
    @pytest.mark.crosszip_parametrize(
        "method",
        ["GET", "POST", "PUT", "DELETE"],
        "token",
        ["valid", "expired"],
    )
    def test_https_methods(self, method, token): ...  # 4 × 2 = 8 tests
```

### Strategy 5: Tiered test suite with custom marks

Keep a fast smoke test always active and gate the full combinatorial matrix
behind a `slow` mark, run only in nightly CI:

```python
import pytest


# Always runs — representative single combination
def test_api_smoke(): ...


# Skipped in fast mode, run on schedule
@pytest.mark.slow
@pytest.mark.crosszip_parametrize(
    "protocol",
    ["http", "https", "ftp", "ssh"],
    "method",
    ["GET", "POST", "PUT", "DELETE"],
)
def test_api_full_matrix(
    protocol, method
): ...  # 4 × 4 = 16 tests, guarded by the slow mark
```

Register the mark in `pyproject.toml` to silence the unknown-mark warning:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
]
```

Run selectively:

```bash
# Fast CI run — skip the full matrix
pytest -m "not slow"

# Nightly run — include everything
pytest -m "slow"
```
