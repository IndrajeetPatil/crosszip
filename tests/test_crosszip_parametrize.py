from itertools import product

import math
import pytest

from crosszip_parametrize import crosszip_parametrize


@pytest.mark.parametrize(
    "params, expected_combinations",
    [
        (("a", [1, 2], "b", [3, 4]), list(product([1, 2], [3, 4]))),
        (("a", [1, 2]), [(1,), (2,)]),
    ],
)
def test_crosszip_parametrize_valid_cases(params, expected_combinations):
    @crosszip_parametrize(*params)
    def test_example(*args):
        assert args in expected_combinations

    _run_test_cases(test_example, expected_combinations)


@pytest.mark.parametrize(
    "params, expected_error, match",
    [
        (
            ("a", [], "b", [3, 4]),
            ValueError,
            "All parameter value lists must be non-empty.",
        ),
        ((), ValueError, "Parameter names and values must be provided."),
        (
            ("a", [1, 2], "b"),
            ValueError,
            "Each parameter name must have a corresponding list of values.",
        ),
        (
            ("a", [], "b", []),
            ValueError,
            "All parameter value lists must be non-empty.",
        ),
        (
            ("a", 1, "b", [3, 4]),
            ValueError,
            "All parameter value lists must be non-empty.",
        ),
    ],
)
def test_crosszip_parametrize_invalid_cases(params, expected_error, match):
    with pytest.raises(expected_error, match=match):
        crosszip_parametrize(*params)


def test_pytest_configure_marker_registration():
    class MockConfig:
        def __init__(self):
            self.lines = []

        def addinivalue_line(self, key, value):
            self.lines.append((key, value))

    config = MockConfig()
    pytest_configure(config)

    assert (
        "markers",
        "crosszip_parametrize: parametrize tests with all combinations of provided parameters",
    ) in config.lines


def _run_test_cases(test_func, cases):
    for case in cases:
        test_func(*case)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "crosszip_parametrize: parametrize tests with all combinations of provided parameters",
    )


def test_pytest_marker_call_count(mocker):
    mock_func = mocker.Mock()

    @crosszip_parametrize(
        "base",
        [2, 10],
        "exponent",
        [-1, 0, 1],
    )
    def test_power_function(base, exponent):
        mock_func(base, exponent)
        result = math.pow(base, exponent)
        assert result == base**exponent

    for base, exponent in [(2, -1), (2, 0), (2, 1), (10, -1), (10, 0), (10, 1)]:
        test_power_function(base, exponent)

    assert mock_func.call_count == 6
