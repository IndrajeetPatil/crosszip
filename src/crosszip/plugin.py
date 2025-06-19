from collections.abc import Sequence
from itertools import product
from typing import Any

import pytest

from .exceptions import (
    PARAMS_COUNT_MISMATCH_ERROR,
    PARAMS_NAME_TYPE_ERROR,
    PARAMS_REQUIRED_ERROR,
    PARAMS_VALUES_TYPE_ERROR,
    CrosszipTypeError,
    CrosszipValueError,
)


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    """
    Register the `crosszip_parametrize` marker with pytest.

    This pytest hook registers the `crosszip_parametrize` marker with pytest. The marker
    is used to parametrize tests with the Cartesian product of parameter values.
    """
    config.addinivalue_line(
        "markers",
        "crosszip_parametrize(*args): mark test to be cross-parametrized",
    )


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """
    Generate parametrized tests using the cross-product of parameter values.

    This pytest hook parametrizes tests based on the `crosszip_parametrize` marker.
    It extracts parameter names and their corresponding lists of values, computes their
    Cartesian product, and parametrizes the test function accordingly.

    Args:
        metafunc (pytest.Metafunc): The test function's metadata provided by pytest.

    Raises:
        CrosszipValueError: If parameter names and values are not provided or their
            lengths do not match.
        CrosszipTypeError: If parameter names are not strings or parameter values are
            empty sequences.

    Example:
        ```python
        import math
        import crosszip
        import pytest


        @pytest.mark.crosszip_parametrize(
            "base",
            [2, 10],
            "exponent",
            [-1, 0, 1],
        )
        def test_power_function(base, exponent):
            result = math.pow(base, exponent)
            assert result == base**exponent


        @pytest.mark.crosszip_parametrize()
        def test_example():
            pass


        # Error: Parameter names and values must be provided.


        @pytest.mark.crosszip_parametrize(
            "x",
            1,
            "y",
            [3, 4],
        )
        def test_example(x, y):
            pass


        # Error: All parameter values must be non-empty sequences.
        ```

    """
    marker = metafunc.definition.get_closest_marker("crosszip_parametrize")
    if marker:
        args: tuple[Any, ...] = marker.args
        param_names: tuple[Any, ...] = args[::2]
        param_values: tuple[Any, ...] = args[1::2]

        validate_parameters(param_names, param_values)

        combinations: list[tuple[Any, ...]] = list(product(*param_values))
        param_names_str: str = ",".join(param_names)
        metafunc.parametrize(param_names_str, combinations)


def validate_parameters(
    param_names: Sequence[Any], param_values: Sequence[Any]
) -> None:
    if not param_names or not param_values:
        raise CrosszipValueError(PARAMS_REQUIRED_ERROR)
    if len(param_names) != len(param_values):
        raise CrosszipValueError(PARAMS_COUNT_MISMATCH_ERROR)
    if not all(isinstance(name, str) for name in param_names):
        raise CrosszipTypeError(PARAMS_NAME_TYPE_ERROR)
    if any(not values for values in param_values):
        raise CrosszipTypeError(PARAMS_VALUES_TYPE_ERROR)
