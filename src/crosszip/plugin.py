from itertools import product
from typing import Any, List, Optional, Sequence, Tuple

import pytest


@pytest.hookimpl(trylast=True)
def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "crosszip_parametrize(*args): mark test to be parametrized with Cartesian product of combinations",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    for item in items:
        marker: Optional[pytest.Mark] = item.get_closest_marker("crosszip_parametrize")
        if marker:
            args: Tuple[Any, ...] = marker.args
            param_names: Tuple[Any, ...] = args[::2]
            param_values: Tuple[Any, ...] = args[1::2]

            if not param_names or not param_values:
                raise ValueError("Parameter names and values must be provided.")
            if len(param_names) != len(param_values):
                raise ValueError(
                    "Each parameter name must have a corresponding list of values."
                )

            # Validate that all parameter names are strings
            if not all(isinstance(name, str) for name in param_names):
                raise TypeError("All parameter names must be strings.")

            # Validate that all parameter values are non-empty sequences
            if any(
                not isinstance(values, Sequence) or not values
                for values in param_values
            ):
                raise TypeError("All parameter values must be non-empty sequences.")

            combinations: List[Tuple[Any, ...]] = list(product(*param_values))
            param_names_str: str = ",".join(param_names)
            new_mark = pytest.mark.parametrize(param_names_str, combinations)
            item.add_marker(new_mark)
