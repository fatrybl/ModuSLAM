from moduslam.external.connections.utils import fill_one_connection
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.imu import Imu, ImuData
from moduslam.measurement_storage.measurements.pose import Pose
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4


def test_imu_before_core(data: ImuData):
    t1, t2 = 0, 1
    m1 = Imu(t1, data)
    core = Pose(t2, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core)

    num_unused, leftovers = fill_one_connection(cluster, [m1], None)

    assert num_unused == 0
    assert leftovers == []
    assert len(cluster.continuous_measurements) == 1


def test_imu_before_core_with_left_limit(data: ImuData):
    t1, t2, t3 = 0, 1, 2
    m1 = Imu(t2, data)
    core = Pose(t3, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core)

    num_unused, leftovers = fill_one_connection(cluster, [m1], t1)

    assert num_unused == 0
    assert leftovers == []
    assert len(cluster.continuous_measurements) == 1
    assert cluster.continuous_measurements[0].time_range.start == t1
    assert cluster.continuous_measurements[0].time_range.stop == cluster.timestamp


def test_imu_after_core(data: ImuData):
    t1, t2 = 0, 1
    m1 = Imu(t2, data)
    core = Pose(t1, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core)

    num_unused, leftovers = fill_one_connection(cluster, [m1], None)

    assert num_unused == 0
    assert leftovers == [m1]
    assert len(cluster.continuous_measurements) == 0


def test_both_same_timestamp(data: ImuData):
    t = 0
    m1 = Imu(t, data)
    core = Pose(t, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(core)

    num_unused, leftovers = fill_one_connection(cluster, [m1], None)

    assert num_unused == 0
    assert leftovers == [m1]
    assert len(cluster.continuous_measurements) == 0

    cluster = MeasurementCluster()
    cluster.add(core)
    num_unused, leftovers = fill_one_connection(cluster, [m1], t)

    assert num_unused == 0
    assert leftovers == [m1]
    assert len(cluster.continuous_measurements) == 0
