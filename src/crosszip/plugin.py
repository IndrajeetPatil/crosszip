from collections.abc import Sequence
from itertools import product
from typing import Any, Final

import pytest


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
        ValueError: If parameter names and values are not provided or their lengths do not match.
        TypeError: If parameter names are not strings or parameter values are empty sequences.

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
        args = marker.args
        param_names = args[::2]
        param_values = args[1::2]

        validate_parameters(param_names, param_values)

        combinations = list(product(*param_values))
        param_names_str = ",".join(param_names)
        metafunc.parametrize(param_names_str, combinations)


PARAMS_REQUIRED_ERROR: Final = "Parameter names and values must be provided."
PARAMS_COUNT_MISMATCH_ERROR: Final = (
    "Each parameter name must have a corresponding list of values."
)
PARAMS_NAME_TYPE_ERROR: Final = "All parameter names must be strings."
PARAMS_VALUES_TYPE_ERROR: Final = "All parameter values must be non-empty sequences."


def validate_parameters(
    param_names: Sequence[str], param_values: Sequence[Sequence[Any]]
) -> None:
    if not param_names or not param_values:
        raise ValueError(PARAMS_REQUIRED_ERROR)
    if len(param_names) != len(param_values):
        raise ValueError(PARAMS_COUNT_MISMATCH_ERROR)
    if not all(isinstance(name, str) for name in param_names):
        raise TypeError(PARAMS_NAME_TYPE_ERROR)
    if any(not values for values in param_values):
        raise TypeError(PARAMS_VALUES_TYPE_ERROR)
