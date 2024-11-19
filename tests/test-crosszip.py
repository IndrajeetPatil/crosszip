import pytest
from crosszip.crosszip import crosszip


@pytest.fixture
def concat_function():
    """Fixture for a basic concatenation function."""
    return lambda a, b, c: f"{a}-{b}-{c}"


@pytest.fixture
def add_function():
    """Fixture for a simple addition function."""
    return lambda a, b, c: a + b + c


@pytest.mark.parametrize(
    "iterable1, iterable2, iterable3, expected",
    [
        (
            [1, 2],
            ["a", "b"],
            [True, False],
            [
                "1-a-True",
                "1-a-False",
                "1-b-True",
                "1-b-False",
                "2-a-True",
                "2-a-False",
                "2-b-True",
                "2-b-False",
            ],
        ),
        (
            (1, 2),
            ("a", "b"),
            (True, False),
            [
                "1-a-True",
                "1-a-False",
                "1-b-True",
                "1-b-False",
                "2-a-True",
                "2-a-False",
                "2-b-True",
                "2-b-False",
            ],
        ),
        (
            {1, 2},
            {"a", "b"},
            {True, False},
            [
                "1-a-True",
                "1-a-False",
                "1-b-True",
                "1-b-False",
                "2-a-True",
                "2-a-False",
                "2-b-True",
                "2-b-False",
            ],
        ),
        (
            "12",
            "ab",
            "xy",
            ["1-a-x", "1-a-y", "1-b-x", "1-b-y", "2-a-x", "2-a-y", "2-b-x", "2-b-y"],
        ),
    ],
)
def test_crosszip_with_iterables(
    concat_function, iterable1, iterable2, iterable3, expected
):
    result = crosszip(concat_function, iterable1, iterable2, iterable3)
    assert result == expected


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


@pytest.mark.parametrize("non_iterable", [123, None, 3.14, True])
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
