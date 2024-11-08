import pytest

from phd.bridge.objects.auxiliary_classes import PseudoMeasurement
from phd.external.utils import get_subsequence


def test_get_subsequence_empty_sequence():
    with pytest.raises(ValueError, match="Empty sequence or invalid limits."):
        get_subsequence([], 0, 10)


def test_get_subsequence_start_greater_than_stop():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")

    with pytest.raises(ValueError, match="Empty sequence or invalid limits."):
        get_subsequence([m1, m2], 2, 1)


def test_get_subsequence_no_timestamps_in_range():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")

    subsequence, start_idx, stop_idx = get_subsequence([m1, m2, m3], 4, 5)

    assert subsequence == []
    assert start_idx == 3
    assert stop_idx == 3


def test_get_subsequence_entire_sequence():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")
    seq = [m1, m2, m3]

    subsequence, start_idx, stop_idx = get_subsequence(seq, 1, 4)

    assert subsequence == seq
    assert start_idx == 0
    assert stop_idx == 3


def test_get_subsequence_single_element():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")

    subsequence, start_idx, stop_idx = get_subsequence([m1, m2, m3], 2, 3)

    assert subsequence == [m2]
    assert start_idx == 1
    assert stop_idx == 2


def test_get_subsequence_equal_start_stop():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")

    subsequence, start_idx, stop_idx = get_subsequence([m1, m2, m3], 2, 2)

    assert subsequence == []
    assert start_idx == 1
    assert stop_idx == 1


def test_get_subsequence_with_duplicate_timestamps():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(2, "c")
    m4 = PseudoMeasurement(3, "d")

    subsequence, start_idx, stop_idx = get_subsequence([m1, m2, m3, m4], 2, 3)

    assert subsequence == [m2, m3]
    assert start_idx == 1
    assert stop_idx == 3


def test_get_subsequence_start_stop_outside_range():
    m1 = PseudoMeasurement(1, "a")
    m2 = PseudoMeasurement(2, "b")
    m3 = PseudoMeasurement(3, "c")
    m4 = PseudoMeasurement(4, "d")

    subsequence, start_idx, stop_idx = get_subsequence([m1, m2, m3, m4], 0, 5)

    assert subsequence == [m1, m2, m3, m4]
    assert start_idx == 0
    assert stop_idx == 4
