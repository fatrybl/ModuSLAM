from moduslam.external.utils import remove_loops
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import (
    PseudoMeasurement,
    SplitPoseOdometry,
)
from moduslam.measurement_storage.measurements.pose_odometry import (
    Odometry as PoseOdometry,
)
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4


def test_remove_loops_with_empty_list():
    empty_combinations: list[list[MeasurementCluster]] = []

    result = remove_loops(empty_combinations)

    assert result == []


def test_remove_loops_with_no_loops():
    odometry = PoseOdometry(1, TimeRange(0, 1), i4x4, i3x3, i3x3)
    t1 = odometry.time_range.start
    t2 = odometry.time_range.stop
    split_odom1 = SplitPoseOdometry(t1, odometry)
    split_odom2 = SplitPoseOdometry(t2, odometry)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(split_odom1)
    cluster2.add(split_odom2)
    combinations = [[cluster1, cluster2]]

    result = remove_loops(combinations)

    assert result == combinations


def test_remove_loops_with_all_loops():
    odometry1 = PoseOdometry(2, TimeRange(1, 2), i4x4, i3x3, i3x3)
    odometry2 = PoseOdometry(4, TimeRange(3, 4), i4x4, i3x3, i3x3)
    splitted_odom1 = SplitPoseOdometry(1, odometry1)
    splitted_odom2 = SplitPoseOdometry(2, odometry1)
    splitted_odom3 = SplitPoseOdometry(3, odometry2)
    splitted_odom4 = SplitPoseOdometry(4, odometry2)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(splitted_odom1)
    cluster1.add(splitted_odom2)  # Loop in cluster1
    cluster2.add(splitted_odom3)
    cluster2.add(splitted_odom4)  # Loop in cluster2
    combinations = [[cluster1], [cluster2]]

    result = remove_loops(combinations)

    assert result == []


def test_remove_loops_with_mixed_combinations():
    odometry1 = PoseOdometry(2, TimeRange(1, 2), i4x4, i3x3, i3x3)
    odometry2 = PoseOdometry(4, TimeRange(3, 4), i4x4, i3x3, i3x3)
    odometry3 = PoseOdometry(6, TimeRange(5, 6), i4x4, i3x3, i3x3)
    splitted_odom1 = SplitPoseOdometry(1, odometry1)
    splitted_odom2 = SplitPoseOdometry(2, odometry1)
    splitted_odom3 = SplitPoseOdometry(3, odometry2)
    splitted_odom4 = SplitPoseOdometry(4, odometry2)
    splitted_odom5 = SplitPoseOdometry(5, odometry3)
    splitted_odom6 = SplitPoseOdometry(6, odometry3)
    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()

    cluster1.add(splitted_odom1)
    cluster1.add(splitted_odom3)
    cluster2.add(splitted_odom2)
    cluster2.add(splitted_odom4)
    cluster3.add(splitted_odom5)
    cluster3.add(splitted_odom6)  # Loop in cluster3
    combinations = [
        [cluster1, cluster2, cluster3],
        [cluster1, cluster2],
    ]

    result = remove_loops(combinations)

    assert result == [[cluster1, cluster2]]


def test_remove_loops_with_single_cluster_with_loops():
    odometry = PoseOdometry(2, TimeRange(1, 2), i4x4, i3x3, i3x3)
    splitted_odom1 = SplitPoseOdometry(1, odometry)
    splitted_odom2 = SplitPoseOdometry(2, odometry)  # Loop
    cluster = MeasurementCluster()
    cluster.add(splitted_odom1)
    cluster.add(splitted_odom2)
    combinations = [[cluster]]

    result = remove_loops(combinations)

    assert result == []


def test_remove_loops_with_no_splitted_odometry():
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    m1 = PseudoMeasurement(1, "value1")
    m2 = PseudoMeasurement(2, "value2")
    cluster1.add(m1)
    cluster2.add(m2)
    combinations = [[cluster1, cluster2]]

    result = remove_loops(combinations)

    assert result == combinations


def test_remove_loops_all_clusters_without_loops():
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    m1, m2 = PseudoMeasurement(1, "value1"), PseudoMeasurement(2, "value2")
    odometry1 = PoseOdometry(2, TimeRange(1, 2), i4x4, i3x3, i3x3)
    odometry2 = PoseOdometry(4, TimeRange(3, 4), i4x4, i3x3, i3x3)
    splitted_odom1 = SplitPoseOdometry(1, odometry1)
    splitted_odom2 = SplitPoseOdometry(2, odometry1)
    splitted_odom3 = SplitPoseOdometry(3, odometry2)
    splitted_odom4 = SplitPoseOdometry(4, odometry2)

    cluster1.add(m1)
    cluster2.add(m2)
    cluster1.add(splitted_odom1)
    cluster1.add(splitted_odom3)
    cluster2.add(splitted_odom2)
    cluster2.add(splitted_odom4)

    combinations = [[cluster1, cluster2]]

    result = remove_loops(combinations)

    assert result == combinations

    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()

    cluster1.add(m1)
    cluster1.add(splitted_odom1)
    cluster1.add(splitted_odom3)
    cluster2.add(m2)
    cluster2.add(splitted_odom2)
    cluster2.add(splitted_odom4)

    combinations = [
        [cluster1, cluster2, cluster3],
        [cluster1, cluster2],
        [cluster2, cluster3],
    ]

    result = remove_loops(combinations)

    assert result == combinations
