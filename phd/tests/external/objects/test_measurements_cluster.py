import pytest

from phd.external.objects.measurements import (
    ContinuousMeasurement,
    CoreMeasurement,
    FakeMeasurement,
)
from phd.external.objects.measurements_cluster import Cluster


def test_empty_cluster_initialization():
    empty_cluster = Cluster()
    assert empty_cluster.is_empty
    assert empty_cluster.core_measurements == []
    assert empty_cluster.continuous_measurements == []
    assert empty_cluster.fake_measurements == []
    assert empty_cluster.measurements == []
    with pytest.raises(ValueError):
        empty_cluster.timestamp
    with pytest.raises(ValueError):
        empty_cluster.time_range


def test_add_core_measurements():
    cluster = Cluster()
    timestamp = 2
    start, stop = 1, 2
    core_measurement1 = CoreMeasurement(timestamp=start, value=1.0)
    core_measurement2 = CoreMeasurement(timestamp=stop, value=2.0)

    cluster.add(core_measurement1)
    cluster.add(core_measurement2)

    assert len(cluster.core_measurements) == 2
    assert cluster.core_measurements[0] == core_measurement1
    assert cluster.core_measurements[1] == core_measurement2
    assert cluster.timestamp == timestamp
    assert cluster.time_range.start == start
    assert cluster.time_range.stop == stop


def test_add_continuous_measurements():
    cluster = Cluster()
    elements = [CoreMeasurement(timestamp=1, value=1.0), CoreMeasurement(timestamp=2, value=2.0)]
    measurement1 = ContinuousMeasurement(elements=elements)
    measurement2 = ContinuousMeasurement(elements=elements)

    cluster.add(measurement1)
    cluster.add(measurement2)

    assert len(cluster.continuous_measurements) == 2
    assert cluster.continuous_measurements[0] == measurement1
    assert cluster.continuous_measurements[1] == measurement2
    assert len(cluster.core_measurements) == 0
    assert len(cluster.fake_measurements) == 0
    assert not cluster.is_empty
    with pytest.raises(ValueError):
        cluster.timestamp
    with pytest.raises(ValueError):
        cluster.time_range


def test_add_fake_measurements():
    cluster = Cluster()
    measurement1 = FakeMeasurement(timestamp=1)
    measurement2 = FakeMeasurement(timestamp=2)

    cluster.add(measurement1)
    cluster.add(measurement2)

    assert len(cluster.fake_measurements) == 2
    assert cluster.fake_measurements[0] == measurement1
    assert cluster.fake_measurements[1] == measurement2
    assert len(cluster.core_measurements) == 0
    assert len(cluster.continuous_measurements) == 0
    assert not cluster.is_empty
    with pytest.raises(ValueError):
        cluster.timestamp
    with pytest.raises(ValueError):
        cluster.time_range


def test_cluster_timestamp():
    cluster = Cluster()
    core_measurements = [
        CoreMeasurement(timestamp=1, value=1.0),
        CoreMeasurement(timestamp=2, value=2.0),
        CoreMeasurement(timestamp=4, value=3.0),
        CoreMeasurement(timestamp=5, value=4.0),
    ]

    for core_measurement in core_measurements:
        cluster.add(core_measurement)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 5
    assert cluster.timestamp == 4

    cluster = Cluster()
    for core_measurement in core_measurements[:-1]:
        cluster.add(core_measurement)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 4
    assert cluster.timestamp == 2


def test_cluster_time_range():
    cluster = Cluster()
    core_measurements = [
        CoreMeasurement(timestamp=1, value=1.0),
        CoreMeasurement(timestamp=2, value=2.0),
        CoreMeasurement(timestamp=3, value=3.0),
    ]

    for core_measurement in core_measurements:
        cluster.add(core_measurement)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 3

    cluster = Cluster()
    core_measurement = CoreMeasurement(timestamp=10, value=1.0)
    cluster.add(core_measurement)

    assert cluster.time_range.start == 10
    assert cluster.time_range.stop == 10


def test_add_mixture_of_measurements():
    cluster = Cluster()
    core_measurement1 = CoreMeasurement(timestamp=1, value=1.0)
    core_measurement2 = CoreMeasurement(timestamp=3, value=1.0)
    continuous_measurement = ContinuousMeasurement(elements=[core_measurement1, core_measurement2])
    fake_measurement = FakeMeasurement(timestamp=2)

    cluster.add(core_measurement1)
    cluster.add(continuous_measurement)
    cluster.add(fake_measurement)
    cluster.add(core_measurement2)

    assert len(cluster.core_measurements) == 2
    assert len(cluster.continuous_measurements) == 1
    assert len(cluster.fake_measurements) == 1
    assert cluster.timestamp == 3
    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 3


def test_remove_all_measurements():
    cluster = Cluster()
    core_measurement1 = CoreMeasurement(timestamp=1, value=1.0)
    core_measurement2 = CoreMeasurement(timestamp=2, value=2.0)
    continuous_measurement = ContinuousMeasurement(elements=[core_measurement1, core_measurement2])
    fake_measurement = FakeMeasurement(timestamp=3)

    cluster.add(core_measurement1)
    cluster.add(continuous_measurement)
    cluster.add(fake_measurement)
    cluster.add(core_measurement2)

    assert len(cluster.core_measurements) == 2
    assert len(cluster.continuous_measurements) == 1
    assert len(cluster.fake_measurements) == 1
    assert not cluster.is_empty

    cluster.remove(core_measurement1)
    cluster.remove(continuous_measurement)
    cluster.remove(fake_measurement)
    cluster.remove(core_measurement2)

    assert len(cluster.core_measurements) == 0
    assert len(cluster.continuous_measurements) == 0
    assert len(cluster.fake_measurements) == 0
    assert cluster.is_empty


def test_remove_core_measurement():
    cluster = Cluster()
    core_measurement1 = CoreMeasurement(timestamp=1, value=1.0)
    core_measurement2 = CoreMeasurement(timestamp=2, value=2.0)
    continuous_measurement = ContinuousMeasurement(elements=[core_measurement1, core_measurement2])
    fake_measurement = FakeMeasurement(timestamp=3)

    cluster.add(core_measurement1)
    cluster.add(continuous_measurement)
    cluster.add(fake_measurement)
    cluster.add(core_measurement2)

    cluster.remove(core_measurement1)

    assert len(cluster.core_measurements) == 1
    assert cluster.core_measurements[0] == core_measurement2
    assert cluster.timestamp == 2
    assert cluster.time_range.start == cluster.time_range.stop == 2
