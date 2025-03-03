import pytest

from src.utils.auxiliary_methods import equal_integers


def test_equal_integers():
    assert equal_integers(0, 0, 0) is True
    assert equal_integers(1, -1, 0) is False
    assert equal_integers(1, 2, 1) is True
    assert equal_integers(3, 1, 1) is False
    with pytest.raises(ValueError):
        assert equal_integers(5, 6, -1) is True
