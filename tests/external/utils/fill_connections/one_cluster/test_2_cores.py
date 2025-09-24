from moduslam.external.connections.utils import fill_one_connection
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.imu import Imu, ImuData
from moduslam.measurement_storage.measurements.pose import Pose
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4


def test_imu_before_cores(data: ImuData):
    t1, t2, t3 = 0, 1, 2
    m1, m2 = Imu(t1, data), Imu(t2, data)
    core1, core2 = Pose(t2, i4x4, i3x3, i3x3), Pose(t3, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core1)
    cluster.add(core2)

    num_unused, leftovers = fill_one_connection(cluster, [m1, m2], None)

    assert num_unused == 0
    assert leftovers == []
    assert len(cluster.continuous_measurements) == 1
    assert cluster.continuous_measurements[0].time_range.start == t1
    assert cluster.continuous_measurements[0].time_range.stop == cluster.timestamp


def test_imu_after_cores(data: ImuData):
    t1, t2, t3 = 0, 1, 2
    m1, m2 = Imu(t2, data), Imu(t3, data)
    core1, core2 = Pose(t1, i4x4, i3x3, i3x3), Pose(t2, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core1)
    cluster.add(core2)

    num_unused, leftovers = fill_one_connection(cluster, [m1, m2], None)

    assert num_unused == 0
    assert leftovers == [m1, m2]
    assert len(cluster.continuous_measurements) == 0


def test_imu_in_between(data: ImuData):
    t1, t2, t3 = 0, 1, 2
    m1, m2 = Imu(t1, data), Imu(t2, data)
    core1, core2 = Pose(t1, i4x4, i3x3, i3x3), Pose(t3, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core1)
    cluster.add(core2)

    num_unused, leftovers = fill_one_connection(cluster, [m1, m2], None)

    assert num_unused == 2
    assert leftovers == []
    assert len(cluster.continuous_measurements) == 0


def test_imu_1_before_1_between(data: ImuData):
    t1, t2, t3 = 0, 1, 2
    m1, m2 = Imu(t1, data), Imu(t2, data)
    core1, core2 = Pose(t2, i4x4, i3x3, i3x3), Pose(t3, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core1)
    cluster.add(core2)

    num_unused, leftovers = fill_one_connection(cluster, [m1, m2], None)

    assert num_unused == 0
    assert leftovers == []
    assert len(cluster.continuous_measurements) == 1
    assert cluster.continuous_measurements[0].time_range.start == t1
    assert cluster.continuous_measurements[0].time_range.stop == cluster.timestamp


def test_imu_1_before_1_between_left_limit(data: ImuData):
    t1, t2, t3, t4 = 0, 1, 2, 3
    m1, m2 = Imu(t2, data), Imu(t3, data)
    core1, core2 = Pose(t3, i4x4, i3x3, i3x3), Pose(t4, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core1)
    cluster.add(core2)

    num_unused, leftovers = fill_one_connection(cluster, [m1, m2], t1)

    assert num_unused == 0
    assert leftovers == []
    assert len(cluster.continuous_measurements) == 1
    assert cluster.continuous_measurements[0].time_range.start == t1
    assert cluster.continuous_measurements[0].time_range.stop == cluster.timestamp


def test_imu_1_before_left_limit(data: ImuData):
    t1, t2, t3 = 0, 1, 2
    m1, m2, m3 = Imu(t1, data), Imu(t2, data), Imu(t3, data)
    core1, core2 = Pose(t2, i4x4, i3x3, i3x3), Pose(t3, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core1)
    cluster.add(core2)

    num_unused, leftovers = fill_one_connection(cluster, [m1, m2, m3], t2)

    assert num_unused == 0
    assert leftovers == [m3]
    assert len(cluster.continuous_measurements) == 1
    assert cluster.continuous_measurements[0].time_range.start == t1
    assert cluster.continuous_measurements[0].time_range.stop == cluster.timestamp
