import pytest
from itertools import product

from crosszip_parametrize import crosszip_parametrize


def test_crosszip_parametrize_happy_path():
    @crosszip_parametrize("a", [1, 2], "b", [3, 4])
    def test_example(a, b):
        assert (a, b) in [(1, 3), (1, 4), (2, 3), (2, 4)]

    _run_test_cases(test_example, product([1, 2], [3, 4]))


def test_crosszip_parametrize_single_parameter():
    @crosszip_parametrize("a", [1, 2])
    def test_example(a):
        assert a in [1, 2]

    _run_test_cases(test_example, [(1,), (2,)])


def test_crosszip_parametrize_empty_values():
    with pytest.raises(
        ValueError,
        match="All parameter value lists must be non-empty.",
    ):
        crosszip_parametrize("a", [], "b", [3, 4])


def test_crosszip_parametrize_empty_names_and_values():
    with pytest.raises(
        ValueError, match="Parameter names and values must be provided."
    ):
        crosszip_parametrize()  # No arguments provided


def test_crosszip_parametrize_mismatched_names_and_values():
    with pytest.raises(
        ValueError,
        match="Each parameter name must have a corresponding list of values.",
    ):
        crosszip_parametrize("a", [1, 2], "b")


def test_crosszip_parametrize_multiple_empty_lists():
    with pytest.raises(
        ValueError,
        match="All parameter value lists must be non-empty.",
    ):
        crosszip_parametrize("a", [], "b", [])


def test_crosszip_parametrize_non_iterable_values():
    with pytest.raises(
        ValueError,
        match="All parameter value lists must be non-empty.",
    ):
        crosszip_parametrize("a", 1, "b", [3, 4])


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
