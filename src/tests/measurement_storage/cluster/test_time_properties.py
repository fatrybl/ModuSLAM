import pytest

from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.auxiliary import FakeMeasurement
from src.utils.auxiliary_dataclasses import TimeRange


def test_with_single_measurement():
    t = 5
    measurement = FakeMeasurement(t)
    cluster = MeasurementCluster()

    cluster.add(measurement)

    assert cluster.timestamp == t
    assert cluster.time_range == TimeRange(t, t)


def test_with_odd_num_measurements():
    t1, t2, t3 = 1, 5, 10
    m1, m2, m3 = FakeMeasurement(t1), FakeMeasurement(t2), FakeMeasurement(t3)
    cluster = MeasurementCluster()

    cluster.add(m1)
    cluster.add(m2)
    cluster.add(m3)

    assert cluster.timestamp == t2
    assert cluster.time_range == TimeRange(t1, t3)


def test_with_even_num_measurements():
    t1, t2, t3, t4 = 1, 5, 10, 15
    measurements = [FakeMeasurement(t) for t in [t1, t2, t3, t4]]
    cluster = MeasurementCluster()

    for m in measurements:
        cluster.add(m)

    assert cluster.timestamp == t3
    assert cluster.time_range == TimeRange(t1, t4)


def test_raises_value_error_for_empty_cluster():
    cluster = MeasurementCluster()

    with pytest.raises(ValueError):
        _ = cluster.timestamp

    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_with_measurements_equal_time():
    """TODO: this test should be modified after Groups update."""
    t1, t2 = 0, 1
    m1 = FakeMeasurement(t1)
    m2 = FakeMeasurement(t1)
    m3 = FakeMeasurement(t2)
    cluster = MeasurementCluster()

    cluster.add(m1)
    cluster.add(m2)
    cluster.add(m3)

    assert cluster.timestamp == t1
    assert cluster.time_range == TimeRange(t1, t2)


def test_add_remove_single_measurement():
    t = 5
    measurement = FakeMeasurement(t)
    cluster = MeasurementCluster()

    cluster.add(measurement)

    assert cluster.timestamp == t
    assert cluster.time_range == TimeRange(t, t)

    cluster.remove(measurement)

    with pytest.raises(ValueError):
        _ = cluster.timestamp
    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_add_remove_multiple_measurements():
    t1, t2, t3 = 1, 5, 10
    m1, m2, m3 = FakeMeasurement(t1), FakeMeasurement(t2), FakeMeasurement(t3)
    cluster = MeasurementCluster()

    cluster.add(m1)
    cluster.add(m2)
    cluster.add(m3)

    assert cluster.timestamp == t2
    assert cluster.time_range == TimeRange(t1, t3)

    cluster.remove(m2)

    assert cluster.timestamp == t3
    assert cluster.time_range == TimeRange(t1, t3)

    cluster.remove(m3)

    assert cluster.timestamp == t1
    assert cluster.time_range == TimeRange(t1, t1)

    cluster.remove(m1)
    with pytest.raises(ValueError):
        _ = cluster.timestamp
    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_add_remove_measurements_with_equal_time():
    """TODO: this test should be modified after Groups update."""

    t1, t2 = 0, 1
    m1 = FakeMeasurement(t1)
    m2 = FakeMeasurement(t1)
    m3 = FakeMeasurement(t2)
    cluster = MeasurementCluster()

    cluster.add(m1)
    cluster.add(m2)
    cluster.add(m3)

    assert cluster.timestamp == t1
    assert cluster.time_range == TimeRange(t1, t2)

    cluster.remove(m1)

    assert cluster.timestamp == t2
    assert cluster.time_range == TimeRange(t1, t2)

    cluster.remove(m2)

    assert cluster.timestamp == t2
    assert cluster.time_range == TimeRange(t2, t2)

    cluster.remove(m3)

    with pytest.raises(ValueError):
        _ = cluster.timestamp
    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_add_remove_measurements_with_even_count():
    t1, t2, t3, t4 = 1, 5, 10, 15
    measurements = [FakeMeasurement(t) for t in [t1, t2, t3, t4]]
    cluster = MeasurementCluster()

    for m in measurements:
        cluster.add(m)

    assert cluster.timestamp == t3
    assert cluster.time_range == TimeRange(t1, t4)

    cluster.remove(measurements[2])

    assert cluster.timestamp == t2
    assert cluster.time_range == TimeRange(t1, t4)

    cluster.remove(measurements[1])

    assert cluster.timestamp == t4
    assert cluster.time_range == TimeRange(t1, t4)

    cluster.remove(measurements[3])

    assert cluster.timestamp == t1
    assert cluster.time_range == TimeRange(t1, t1)

    cluster.remove(measurements[0])

    with pytest.raises(ValueError):
        _ = cluster.timestamp
    with pytest.raises(ValueError):
        _ = cluster.time_range
