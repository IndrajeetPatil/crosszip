import pytest


@pytest.mark.crosszip_parametrize("a", [1, 2], "b", [3, 4])
def test_example(a, b):
    assert (a, b) in [(1, 3), (1, 4), (2, 3), (2, 4)]
