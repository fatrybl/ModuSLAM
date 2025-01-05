import pytest

from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.auxiliary import (
    FakeMeasurement,
    PseudoMeasurement,
)
from src.measurement_storage.measurements.continuous import ContinuousMeasurement


def test_empty_cluster_initialization():
    empty_cluster = MeasurementCluster()
    assert empty_cluster.empty
    assert empty_cluster.core_measurements == []
    assert empty_cluster.continuous_measurements == []
    assert empty_cluster.fake_measurements == []
    assert empty_cluster.measurements == []

    with pytest.raises(ValueError):
        _ = empty_cluster.timestamp

    with pytest.raises(ValueError):
        _ = empty_cluster.time_range


def test_add_core_measurements():
    cluster = MeasurementCluster()
    timestamp = 2
    start, stop = 1, 2
    m1, m2 = PseudoMeasurement(start, 1.0), PseudoMeasurement(stop, 2.0)

    cluster.add(m1)
    cluster.add(m2)

    assert len(cluster.core_measurements) == 2
    assert cluster.core_measurements[0] == m1
    assert cluster.core_measurements[1] == m2
    assert cluster.timestamp == timestamp
    assert cluster.time_range.start == start
    assert cluster.time_range.stop == stop


def test_add_continuous_measurements():
    cluster = MeasurementCluster()
    measurements = [PseudoMeasurement(1, 1.0), PseudoMeasurement(2, 2.0)]
    continuous1 = ContinuousMeasurement(measurements)
    continuous2 = ContinuousMeasurement(measurements)

    cluster.add(continuous1)
    cluster.add(continuous2)

    assert len(cluster.continuous_measurements) == 2
    assert cluster.continuous_measurements[0] == continuous1
    assert cluster.continuous_measurements[1] == continuous2
    assert len(cluster.core_measurements) == 0
    assert len(cluster.fake_measurements) == 0
    assert not cluster.empty
    with pytest.raises(ValueError):
        _ = cluster.timestamp
    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_add_fake_measurements():
    cluster = MeasurementCluster()
    m1, m2 = FakeMeasurement(timestamp=1), FakeMeasurement(timestamp=2)

    cluster.add(m1)
    cluster.add(m2)

    assert len(cluster.fake_measurements) == 2
    assert cluster.fake_measurements[0] == m1
    assert cluster.fake_measurements[1] == m2
    assert len(cluster.core_measurements) == 0
    assert len(cluster.continuous_measurements) == 0
    assert not cluster.empty
    assert cluster.timestamp == 2
    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 2


def test_cluster_timestamp():
    cluster = MeasurementCluster()
    core_measurements = [
        PseudoMeasurement(1, 1.0),
        PseudoMeasurement(2, 2.0),
        PseudoMeasurement(4, 3.0),
        PseudoMeasurement(5, 4.0),
    ]

    for core_measurement in core_measurements:
        cluster.add(core_measurement)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 5
    assert cluster.timestamp == 4

    cluster = MeasurementCluster()
    for core_measurement in core_measurements[:-1]:
        cluster.add(core_measurement)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 4
    assert cluster.timestamp == 2


def test_cluster_time_range():
    cluster = MeasurementCluster()
    core_measurements = [
        PseudoMeasurement(1, 1.0),
        PseudoMeasurement(2, 2.0),
        PseudoMeasurement(3, 3.0),
    ]

    for core_measurement in core_measurements:
        cluster.add(core_measurement)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 3

    cluster = MeasurementCluster()
    core_measurement = PseudoMeasurement(10, 1.0)
    cluster.add(core_measurement)

    assert cluster.time_range.start == 10
    assert cluster.time_range.stop == 10


def test_add_mixture_of_measurements():
    cluster = MeasurementCluster()
    core1 = PseudoMeasurement(1, 1.0)
    core2 = PseudoMeasurement(3, 1.0)
    continuous = ContinuousMeasurement(measurements=[core1, core2])
    fake = FakeMeasurement(timestamp=2)

    cluster.add(core1)
    cluster.add(continuous)
    cluster.add(fake)
    cluster.add(core2)

    assert len(cluster.measurements) == 4
    assert len(cluster.core_measurements) == 2
    assert len(cluster.continuous_measurements) == 1
    assert len(cluster.fake_measurements) == 1
    assert cluster.timestamp == 2
    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 3


def test_remove_all_measurements():
    cluster = MeasurementCluster()
    core1 = PseudoMeasurement(1, 1.0)
    core2 = PseudoMeasurement(2, 2.0)
    continuous = ContinuousMeasurement(measurements=[core1, core2])
    fake = FakeMeasurement(timestamp=3)

    cluster.add(core1)
    cluster.add(continuous)
    cluster.add(fake)
    cluster.add(core2)

    assert len(cluster.core_measurements) == 2
    assert len(cluster.continuous_measurements) == 1
    assert len(cluster.fake_measurements) == 1
    assert not cluster.empty

    cluster.remove(core1)
    cluster.remove(continuous)
    cluster.remove(fake)
    cluster.remove(core2)

    assert (
        len(cluster.measurements)
        == len(cluster.core_measurements)
        == len(cluster.continuous_measurements)
        == len(cluster.fake_measurements)
        == 0
    )
    assert cluster.empty


def test_remove_core_measurement():
    cluster = MeasurementCluster()
    core1 = PseudoMeasurement(1, 1.0)
    core2 = PseudoMeasurement(2, 2.0)
    continuous = ContinuousMeasurement(measurements=[core1, core2])
    fake = FakeMeasurement(timestamp=3)

    cluster.add(fake)
    cluster.add(core1)
    cluster.add(continuous)
    cluster.add(core2)

    cluster.remove(core1)

    assert len(cluster.core_measurements) == 1
    assert len(cluster.fake_measurements) == 1
    assert cluster.core_measurements[0] == core2
    assert cluster.timestamp == 3
    assert cluster.time_range.start == 2
    assert cluster.time_range.stop == 3
