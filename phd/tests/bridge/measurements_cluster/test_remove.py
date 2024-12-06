import pytest

from phd.measurements.auxiliary_classes import FakeMeasurement
from phd.measurements.cluster import Cluster
from phd.measurements.processed import ContinuousMeasurement
from phd.moduslam.utils.exceptions import ValidationError


def test_remove_non_existing():
    cluster = Cluster()

    with pytest.raises(ValidationError):
        cluster.remove(FakeMeasurement(0))


def test_remove_existing():
    t1 = 1
    m1 = FakeMeasurement(t1)
    cluster = Cluster()

    cluster.add(m1)

    cluster.remove(m1)

    assert cluster.empty is True
    assert m1 not in cluster
    assert cluster.measurements == []
    assert cluster.fake_measurements == []

    with pytest.raises(ValueError):
        cluster.timestamp
    with pytest.raises(ValueError):
        cluster.time_range


def test_remove_continuous_measurement():
    t1 = 1
    continuous_measurement = ContinuousMeasurement([FakeMeasurement(t1)])
    cluster = Cluster()

    cluster.add(continuous_measurement)

    cluster.remove(continuous_measurement)

    assert cluster.empty is True
    assert continuous_measurement not in cluster
    assert cluster.continuous_measurements == []

    with pytest.raises(ValueError):
        cluster.timestamp
    with pytest.raises(ValueError):
        cluster.time_range


def test_remove_last_measurement_updates_timestamp():
    t1 = 1
    m1 = FakeMeasurement(t1)
    cluster = Cluster()

    cluster.add(m1)
    assert cluster.timestamp == t1

    cluster.remove(m1)

    assert cluster.empty is True
    assert m1 not in cluster
    assert cluster.measurements == []
    assert cluster.fake_measurements == []

    with pytest.raises(ValueError):
        cluster.timestamp
    with pytest.raises(ValueError):
        cluster.time_range


def test_remove_and_readd_same_measurement():
    t1 = 1
    m1 = FakeMeasurement(t1)
    cluster = Cluster()

    cluster.add(m1)

    assert m1 in cluster
    assert cluster.timestamp == t1
    assert cluster.time_range.start == cluster.time_range.stop == t1

    cluster.remove(m1)

    assert cluster.empty is True
    assert m1 not in cluster
    assert cluster.measurements == []
    assert cluster.fake_measurements == []
    with pytest.raises(ValueError):
        cluster.timestamp
    with pytest.raises(ValueError):
        cluster.time_range

    cluster.add(m1)
    assert cluster.empty is False
    assert m1 in cluster
    assert cluster.timestamp == t1
    assert cluster.time_range.start == cluster.time_range.stop == t1
