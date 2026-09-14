"""Benchmark materialized Cartesian products with inexpensive callbacks."""

from __future__ import annotations

import operator
from typing import TYPE_CHECKING

import pytest

from crosszip import crosszip

if TYPE_CHECKING:
    from pytest_codspeed.plugin import BenchmarkFixture


@pytest.mark.parametrize("size", [10, 100], ids=["small", "large"])
def test_numeric_product(benchmark: BenchmarkFixture, size: int) -> None:
    values = range(size)
    expected = [left + right for left in values for right in values]
    result = benchmark(crosszip, operator.add, values, values)
    assert result == expected


def test_three_iterables(benchmark: BenchmarkFixture) -> None:
    values = range(20)

    def add_three(left: int, middle: int, right: int) -> int:
        return left + middle + right

    expected = [
        left + middle + right
        for left in values
        for middle in values
        for right in values
    ]
    assert benchmark(crosszip, add_three, values, values, values) == expected


def test_generator_inputs(benchmark: BenchmarkFixture) -> None:
    # Recreate one-shot inputs on every invocation, including CodSpeed warmup.
    def run() -> list[int]:
        return crosszip(operator.mul, iter(range(50)), iter(range(50)))

    expected = [left * right for left in range(50) for right in range(50)]
    assert benchmark(run) == expected
