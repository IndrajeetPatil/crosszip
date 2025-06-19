import pytest
from _pytest.pytester import Pytester

pytest_plugins = ["pytester"]


@pytest.mark.crosszip_parametrize("a", [1, 2], "b", [3, 4])
def test_example(a: int, b: int) -> None:
    assert (a, b) in {(1, 3), (1, 4), (2, 3), (2, 4)}


def test_crosszip_parametrize(pytester: Pytester) -> None:
    """Test basic functionality with two parameters."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize(
        "x",
        [1, 2],
        "y",
        [3, 4],
    )
    def test_example(x, y):
        assert True
    """)

    result = pytester.runpytest()
    result.assert_outcomes(passed=4)


def test_single_parameter(pytester: Pytester) -> None:
    """Test with a single parameter."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize(
        "x",
        [1, 2, 3],
    )
    def test_example(x):
        assert x[0] in [1, 2, 3]
    """)

    result = pytester.runpytest()
    result.assert_outcomes(passed=3)


def test_invalid_parameter_name(pytester: Pytester) -> None:
    """Test with a non-string parameter name."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize(
        123,
        [1, 2],
        "y",
        [3, 4],
    )
    def test_example(x, y):
        pass
    """)

    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(["*TypeError: All parameter names must be strings.*"])


def test_missing_parameter_values(pytester: Pytester) -> None:
    """Test with mismatched parameter names and values."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize(
        "x",
        [1, 2],
        "y",
    )
    def test_example(x, y):
        pass
    """)

    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(
        [
            "*ValueError: Each parameter name must have a corresponding list of "
            "values.*",
        ]
    )


def test_empty_parameter_values(pytester: Pytester) -> None:
    """Test with empty parameter values."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize(
        "x",
        [],
        "y",
        [3, 4],
    )
    def test_example(x, y):
        pass
    """)

    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(
        [
            "*TypeError: All parameter values must be non-empty sequences.*",
        ]
    )


def test_non_sequence_parameter_values(pytester: Pytester) -> None:
    """Test with non-sequence parameter values."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize(
        "x",
        1,
        "y",
        [3, 4],
    )
    def test_example(x, y):
        pass
    """)

    result = pytester.runpytest()
    result.assert_outcomes(errors=1)


def test_no_parameters(pytester: Pytester) -> None:
    """Test with no parameters provided."""
    pytester.makepyfile("""
    import pytest

    @pytest.mark.crosszip_parametrize()
    def test_example():
        pass
    """)

    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    result.stdout.fnmatch_lines(
        [
            "*ValueError: Parameter names and values must be provided.*",
        ]
    )


def test_parameter_combinations(pytester: Pytester) -> None:
    """Test that the Cartesian product of parameters is correct."""
    pytester.makepyfile("""
    import pytest

    collected_params = []

    @pytest.mark.crosszip_parametrize(
        "x",
        [1, 2],
        "y",
        [3, 4],
        "z",
        [5, 6],
    )
    def test_example(x, y, z):
        collected_params.append((x, y, z))
        assert True

    def test_collected_params():
        expected_params = [
            (1, 3, 5), (1, 3, 6),
            (1, 4, 5), (1, 4, 6),
            (2, 3, 5), (2, 3, 6),
            (2, 4, 5), (2, 4, 6),
        ]
        assert collected_params == expected_params
    """)

    result = pytester.runpytest()
    result.assert_outcomes(passed=9)
