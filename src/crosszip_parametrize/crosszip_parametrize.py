from collections.abc import Callable
from itertools import product
from typing import Any

import pytest


def crosszip_parametrize(
    *args: str | list[Any],
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """A decorator that parametrizes over all possible combinations of provided parameters.

    Usage:
        @crosszip_parametrize('a', [1, 2], 'b', [3, 4])
        def test_example(a, b):
            ...

    This will run the test with all combinations:
        (a=1, b=3), (a=1, b=4), (a=2, b=3), (a=2, b=4)
    """
    param_names = args[::2]
    param_values = args[1::2]

    if not param_names or not param_values:
        raise ValueError("Parameter names and values must be provided.")

    if len(param_names) != len(param_values):
        raise ValueError(
            "Each parameter name must have a corresponding list of values.",
        )

    if any(not isinstance(values, list) or not values for values in param_values):
        raise ValueError("All parameter value lists must be non-empty.")

    # Compute the Cartesian product of parameter values
    combinations = list(product(*param_values))

    param_names_str = ",".join(str(name) for name in param_names)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        return pytest.mark.parametrize(param_names_str, combinations)(func)

    return decorator
