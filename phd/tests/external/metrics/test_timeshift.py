from phd.external.metrics.timeshift import TimeShift
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.auxiliary import (
    FakeMeasurement,
    PseudoMeasurement,
)
from phd.measurement_storage.measurements.continuous import ContinuousMeasurement
from phd.measurement_storage.measurements.imu import ContinuousImu, Imu, ImuData
from phd.moduslam.utils.auxiliary_objects import zero_vector3


def test_timeshift():
    m1, m2, m3 = PseudoMeasurement(0), PseudoMeasurement(1), PseudoMeasurement(2)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(m1)
    c2.add(m2)
    c2.add(m3)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 1


def test_timeshift_empty_clusters():
    time_shift = TimeShift.compute([])

    assert time_shift == 0


def test_timeshift_cluster_with_1_measurement():
    m1, m2 = PseudoMeasurement(0), PseudoMeasurement(3)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(m1)
    c2.add(m2)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 0


def test_timeshift_with_fake_measurement():
    m1, m2 = PseudoMeasurement(0), PseudoMeasurement(1)
    m3 = FakeMeasurement(2)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(m1)
    c1.add(m2)
    c2.add(m3)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 1


def test_timeshift_only_fakes():
    m1, m2, m3, m4 = FakeMeasurement(0), FakeMeasurement(1), FakeMeasurement(2), FakeMeasurement(3)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(m1)
    c1.add(m2)
    c2.add(m3)
    c2.add(m4)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 2


def test_timeshift_continuous_does_not_effect():
    m1, m2, m3 = PseudoMeasurement(0), PseudoMeasurement(1), PseudoMeasurement(2)
    m4, m5, m6 = FakeMeasurement(0), FakeMeasurement(1), FakeMeasurement(2)
    cont = ContinuousMeasurement[PseudoMeasurement]([m1, m2, m3])
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(cont)
    c1.add(m4)
    c2.add(m5)
    c2.add(m6)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 1


def test_timeshift_continuous_effects():
    data = ImuData(zero_vector3, zero_vector3)
    imu1, imu2, imu3 = Imu(1, data), Imu(2, data), Imu(3, data)
    continuous = ContinuousImu([imu1, imu2, imu3], start=0, stop=4)
    m4, m5, m6 = FakeMeasurement(0), FakeMeasurement(1), FakeMeasurement(2)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(continuous)
    c1.add(m4)
    c2.add(m5)
    c2.add(m6)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 1 + 1


def test_timeshift_multiple_continuous_effects():
    data = ImuData(zero_vector3, zero_vector3)
    imu1, imu2, imu3 = Imu(1, data), Imu(2, data), Imu(3, data)
    continuous1 = ContinuousImu([imu1, imu2], start=0, stop=2)
    continuous2 = ContinuousImu([imu1, imu2, imu3], start=0, stop=4)
    m4, m5, m6 = FakeMeasurement(0), FakeMeasurement(1), FakeMeasurement(2)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(continuous1)
    c1.add(m4)
    c2.add(continuous2)
    c2.add(m5)
    c2.add(m6)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 1 + 1 + 1


def test_timeshift_continuous_equal_limits():
    data = ImuData(zero_vector3, zero_vector3)
    imu1, imu2, imu3 = Imu(1, data), Imu(2, data), Imu(3, data)
    continuous1 = ContinuousImu([imu1, imu2], start=1, stop=2)
    continuous2 = ContinuousImu([imu1, imu2, imu3], start=1, stop=3)
    m4, m5, m6 = FakeMeasurement(0), FakeMeasurement(1), FakeMeasurement(2)
    c1, c2 = MeasurementCluster(), MeasurementCluster()
    c1.add(continuous1)
    c1.add(m4)
    c2.add(continuous2)
    c2.add(m5)
    c2.add(m6)
    clusters = [c1, c2]

    time_shift = TimeShift.compute(clusters)

    assert time_shift == 1
