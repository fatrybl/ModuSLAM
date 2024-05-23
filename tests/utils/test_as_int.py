import pytest

from slam.utils.auxiliary_methods import to_int


def test_as_int_with_integer_string():
    assert to_int("123") == 123


def test_as_int_with_float_string():
    with pytest.raises(ValueError):
        to_int("123.45")


def test_as_int_with_non_numeric_string():
    with pytest.raises(ValueError):
        to_int("abc")


def test_as_int_with_empty_string():
    with pytest.raises(ValueError):
        to_int("")
