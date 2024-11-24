import json
import math

import pytest

from crosszip.crosszip import crosszip


@pytest.fixture
def concat_function():
    """Fixture for a basic concatenation function."""
    return lambda a, b, c: f"{a}-{b}-{c}"


@pytest.mark.parametrize(
    "iterable1, iterable2, iterable3, snapshot_name",
    [
        ([1, 2], ["a", "b"], [True, False], "list_inputs"),
        ((1, 2), ("a", "b"), (True, False), "tuple_inputs"),
        ("12", "ab", "xy", "string_inputs"),
    ],
)
def test_crosszip_with_iterables(
    snapshot,
    concat_function,
    iterable1,
    iterable2,
    iterable3,
    snapshot_name,
):
    result = crosszip(concat_function, iterable1, iterable2, iterable3)
    snapshot_json = json.dumps(result, indent=2, sort_keys=True)
    snapshot.assert_match(snapshot_json, f"{snapshot_name}.json")


@pytest.mark.parametrize(
    "iterable1, iterable2, expected",
    [
        (range(1, 3), "ab", ["1-a", "1-b", "2-a", "2-b"]),
    ],
)
def test_crosszip_with_range_and_string(iterable1, iterable2, expected):
    result = crosszip(lambda a, b: f"{a}-{b}", iterable1, iterable2)
    assert result == expected


def test_crosszip_with_generator():
    def gen():
        yield 1
        yield 2

    iterable1 = gen()
    iterable2 = [3, 4]
    iterable3 = ["a", "b"]

    result = crosszip(lambda a, b, c: f"{a}-{b}-{c}", iterable1, iterable2, iterable3)
    expected = ["1-3-a", "1-3-b", "1-4-a", "1-4-b", "2-3-a", "2-3-b", "2-4-a", "2-4-b"]
    assert result == expected


def test_crosszip_with_sets():
    iterable1 = {1, 2}
    iterable2 = {"a", "b"}
    iterable3 = {"x", "y"}

    result = crosszip(lambda a, b, c: f"{a}-{b}-{c}", iterable1, iterable2, iterable3)
    expected = [
        "1-a-x",
        "1-a-y",
        "1-b-x",
        "1-b-y",
        "2-a-x",
        "2-a-y",
        "2-b-x",
        "2-b-y",
    ]
    # sets are unordered, so we need to sort the results
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize("non_iterable", [123, None, math.pi, True])
def test_crosszip_with_non_iterable(non_iterable):
    with pytest.raises(
        TypeError,
        match=f"Expected an iterable, but got {type(non_iterable).__name__}: {non_iterable}",
    ):
        crosszip(lambda a: a, non_iterable)


@pytest.mark.parametrize(
    "iterable1, iterable2, expected_length",
    [
        (range(100), ["a", "b"], 200),
    ],
)
def test_crosszip_large_combinations(iterable1, iterable2, expected_length):
    result = crosszip(lambda a, b: f"{a}-{b}", iterable1, iterable2)
    assert len(result) == expected_length
