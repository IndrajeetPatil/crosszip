import pytest
from _pytest.pytester import Pytester

from crosszip.exceptions import (
    PARAMS_COUNT_MISMATCH_ERROR,
    PARAMS_NAME_TYPE_ERROR,
    PARAMS_REQUIRED_ERROR,
    PARAMS_VALUES_TYPE_ERROR,
    CrosszipTypeError,
    CrosszipValueError,
)
from crosszip.plugin import validate_parameters

pytest_plugins = ["pytester"]


@pytest.mark.crosszip_parametrize("a", [1, 2], "b", [3, 4])
def test_example(a: int, b: int) -> None:
    # This decorator invocation itself is the coverage — if the plugin
    # stopped recognising the `crosszip_parametrize` marker name, pytest
    # would raise "fixture 'a' not found" during collection and this test
    # would fail. That kills mutations that swap the literal marker name.
    assert (a, b) in {(1, 3), (1, 4), (2, 3), (2, 4)}


# Pair the crosszip marker with an unrelated one so a plugin that fetches ANY
# marker (via ``get_closest_marker(None)``) would grab ``pytest.mark.skipif`` —
# whose args are ``(False, "…")`` — and try to parametrise with those. That
# produces the wrong test cases (or crashes), so this test fails.
@pytest.mark.skipif(condition=False, reason="always run — see docstring above")
@pytest.mark.crosszip_parametrize("x", [10, 20], "y", ["a", "b"])
def test_example_with_extra_marker(x: int, y: str) -> None:
    assert x in {10, 20}
    assert y in {"a", "b"}


# Direct unit tests for `validate_parameters` — the pytester-based end-to-end
# tests run in a subprocess and therefore do not exercise the mutated in-process
# module, so we assert each guard branch directly against the installed plugin.


def test_validate_parameters_both_empty_raises_required() -> None:
    with pytest.raises(CrosszipValueError, match=PARAMS_REQUIRED_ERROR):
        validate_parameters((), ())


def test_validate_parameters_only_names_empty_raises_required() -> None:
    # Kills the mutation that weakens `or` to `and` — with `and`, this
    # case (names empty, values non-empty) would slip through and hit the
    # count-mismatch branch instead.
    with pytest.raises(CrosszipValueError, match=PARAMS_REQUIRED_ERROR):
        validate_parameters((), ([1, 2],))


def test_validate_parameters_only_values_empty_raises_required() -> None:
    with pytest.raises(CrosszipValueError, match=PARAMS_REQUIRED_ERROR):
        validate_parameters(("x",), ())


def test_validate_parameters_count_mismatch_raises() -> None:
    with pytest.raises(CrosszipValueError, match=PARAMS_COUNT_MISMATCH_ERROR):
        validate_parameters(("x", "y"), ([1, 2],))


def test_validate_parameters_non_string_name_raises_type() -> None:
    with pytest.raises(CrosszipTypeError, match=PARAMS_NAME_TYPE_ERROR):
        validate_parameters((123,), ([1, 2],))


def test_validate_parameters_empty_values_raises_type() -> None:
    with pytest.raises(CrosszipTypeError, match=PARAMS_VALUES_TYPE_ERROR):
        validate_parameters(("x",), ([],))


def test_validate_parameters_valid_arguments_return_none() -> None:
    # Positive path — the function returns None and does not raise.
    assert validate_parameters(("x", "y"), ([1, 2], [3, 4])) is None


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


def test_crosszip_parametrize_looked_up_by_name(pytester: Pytester) -> None:
    """The plugin must look the marker up by its exact name.

    A test decorated with an unrelated custom marker in addition to the
    crosszip marker would trick a plugin that fetches any marker (e.g.
    ``get_closest_marker(None)``) into parametrising against the wrong
    marker's args. This test wires up a benign extra marker; if the
    plugin does NOT filter by name, the plugin will either explode or
    generate the wrong test cases and the outcome count will not match.
    """
    pytester.makepyfile("""
    import pytest

    @pytest.mark.custom_unrelated("junk")
    @pytest.mark.crosszip_parametrize(
        "x",
        [1, 2],
        "y",
        [3, 4],
    )
    def test_example(x, y):
        assert x in (1, 2)
        assert y in (3, 4)
    """)
    pytester.makefile(
        ".ini",
        pytest="[pytest]\nmarkers =\n    custom_unrelated: extra marker\n",
    )

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
    result.stdout.fnmatch_lines([
        "*ValueError: Each parameter name must have a corresponding list of values.*",
    ])


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
    result.stdout.fnmatch_lines([
        "*TypeError: All parameter values must be non-empty sequences.*",
    ])


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
    result.stdout.fnmatch_lines([
        "*ValueError: Parameter names and values must be provided.*",
    ])


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
