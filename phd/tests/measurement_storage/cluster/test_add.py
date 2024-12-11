import pytest

from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.auxiliary import (
    FakeMeasurement,
    PseudoMeasurement,
)
from phd.measurement_storage.measurements.continuous import ContinuousMeasurement
from phd.moduslam.utils.exceptions import ValidationError


def test_add_existing_measurement():
    t1 = 1
    m1 = FakeMeasurement(t1)
    cluster = MeasurementCluster()

    cluster.add(m1)

    with pytest.raises(ValidationError):
        cluster.add(m1)


def test_add_continuous():
    continuous_measurement = ContinuousMeasurement([PseudoMeasurement(0)])
    cluster = MeasurementCluster()

    cluster.add(continuous_measurement)

    assert continuous_measurement in cluster
    assert continuous_measurement in cluster.continuous_measurements
    assert cluster.continuous_measurements == [continuous_measurement]
    assert cluster.measurements == [continuous_measurement]
    assert cluster.fake_measurements == []
    assert cluster.core_measurements == []
    assert cluster.empty is False
    with pytest.raises(ValueError):
        _ = cluster.timestamp
    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_add_fake():
    t1 = 1
    m1 = FakeMeasurement(t1)
    cluster = MeasurementCluster()

    cluster.add(m1)

    assert m1 in cluster
    assert m1 in cluster.measurements
    assert cluster.core_measurements == []
    assert cluster.fake_measurements == [m1]
    assert cluster.continuous_measurements == []
    assert cluster.empty is False
    assert cluster.timestamp == t1
    assert cluster.time_range.start == t1 and cluster.time_range.stop == t1


def test_add_continuous_does_not_update_timestamp_and_time_range():
    m1 = PseudoMeasurement(0)
    continuous, fake = ContinuousMeasurement([m1]), FakeMeasurement(1)
    cluster = MeasurementCluster()

    cluster.add(fake)
    initial_timestamp = cluster.timestamp
    initial_time_range = cluster.time_range

    cluster.add(continuous)

    assert continuous in cluster
    assert fake in cluster
    assert cluster.timestamp == initial_timestamp
    assert cluster.time_range == initial_time_range


def test_add_correctly_updates_time():
    t1, t2 = 1, 2
    m1, m2 = FakeMeasurement(t1), FakeMeasurement(t2)
    cluster = MeasurementCluster()

    cluster.add(m1)
    cluster.add(m2)

    assert m1 in cluster and m2 in cluster
    assert cluster.timestamp == t2
    assert cluster.time_range.start == t1 and cluster.time_range.stop == t2


def test_add_maintains_order_of_continuous_measurements():
    t1, t2 = 1, 2
    m1, m2 = PseudoMeasurement(t1), PseudoMeasurement(t2)
    continuous_measurement1 = ContinuousMeasurement([m1])
    continuous_measurement2 = ContinuousMeasurement([m2])
    cluster = MeasurementCluster()

    cluster.add(continuous_measurement1)
    cluster.add(continuous_measurement2)

    assert cluster.continuous_measurements == [continuous_measurement1, continuous_measurement2]


def test_add_maintains_order():
    t1, t2, t3 = 1, 2, 3
    m1, m2, m3 = FakeMeasurement(t1), FakeMeasurement(t2), PseudoMeasurement(t3)
    cluster = MeasurementCluster()

    cluster.add(m1)
    cluster.add(m2)
    cluster.add(m3)

    assert cluster.measurements == [m1, m2, m3]
    assert cluster.continuous_measurements == []
    assert cluster.fake_measurements == [m1, m2]
    assert cluster.core_measurements == [m3]
    assert cluster.empty is False
    assert cluster.timestamp == t2
    assert cluster.time_range.start == t1 and cluster.time_range.stop == t3
