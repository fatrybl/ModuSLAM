from phd.external.objects.measurements import (
    CoreMeasurement,
    Odometry,
    SplittedOdometry,
)
from phd.external.objects.measurements_cluster import Cluster
from phd.external.utils import remove_loops


def test_remove_loops_with_empty_list():
    empty_combinations: list[list[Cluster]] = []
    result = remove_loops(empty_combinations)
    assert result == []


def test_remove_loops_with_no_loops():
    odometry = Odometry(1, 2, "value")
    splitted_odom1 = SplittedOdometry(1, "value", odometry)
    splitted_odom2 = SplittedOdometry(2, "value", odometry)
    cluster1, cluster2 = Cluster(), Cluster()
    cluster1.add(splitted_odom1)
    cluster2.add(splitted_odom2)
    combinations = [[cluster1, cluster2]]

    result = remove_loops(combinations)
    assert result == combinations


def test_remove_loops_with_all_loops():
    odometry1 = Odometry(1, 2, "value1")
    odometry2 = Odometry(3, 4, "value2")
    splitted_odom1 = SplittedOdometry(1, "value1", odometry1)
    splitted_odom2 = SplittedOdometry(2, "value1", odometry1)
    splitted_odom3 = SplittedOdometry(3, "value2", odometry2)
    splitted_odom4 = SplittedOdometry(4, "value2", odometry2)
    cluster1, cluster2 = Cluster(), Cluster()
    cluster1.add(splitted_odom1)
    cluster1.add(splitted_odom2)  # Loop in cluster1
    cluster2.add(splitted_odom3)
    cluster2.add(splitted_odom4)  # Loop in cluster2
    combinations = [[cluster1], [cluster2]]

    result = remove_loops(combinations)
    assert result == []


def test_remove_loops_with_mixed_combinations():
    odometry1 = Odometry(1, 2, "value1")
    odometry2 = Odometry(3, 4, "value2")
    odometry3 = Odometry(5, 6, "value3")
    splitted_odom1 = SplittedOdometry(1, "value1", odometry1)
    splitted_odom2 = SplittedOdometry(2, "value1", odometry1)
    splitted_odom3 = SplittedOdometry(3, "value2", odometry2)
    splitted_odom4 = SplittedOdometry(4, "value2", odometry2)
    splitted_odom5 = SplittedOdometry(5, "value3", odometry3)
    splitted_odom6 = SplittedOdometry(6, "value3", odometry3)
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
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
    odometry = Odometry(1, 2, "value")
    splitted_odom1 = SplittedOdometry(1, "value", odometry)
    splitted_odom2 = SplittedOdometry(2, "value", odometry)  # Loop
    cluster = Cluster()
    cluster.add(splitted_odom1)
    cluster.add(splitted_odom2)
    combinations = [[cluster]]

    result = remove_loops(combinations)
    assert result == []


def test_remove_loops_with_no_splitted_odometry():
    cluster1, cluster2 = Cluster(), Cluster()
    m1 = CoreMeasurement(1, "value1")
    m2 = CoreMeasurement(2, "value2")
    cluster1.add(m1)
    cluster2.add(m2)
    combinations = [[cluster1, cluster2]]

    result = remove_loops(combinations)
    assert result == combinations


def test_remove_loops_all_clusters_without_loops():
    cluster1, cluster2 = Cluster(), Cluster()
    m1, m2 = CoreMeasurement(1, "value1"), CoreMeasurement(2, "value2")
    odometry1, odometry2 = Odometry(1, 2, "value1"), Odometry(3, 4, "value2")
    splitted_odom1 = SplittedOdometry(1, "value1", odometry1)
    splitted_odom2 = SplittedOdometry(2, "value1", odometry1)
    splitted_odom3 = SplittedOdometry(3, "value2", odometry2)
    splitted_odom4 = SplittedOdometry(4, "value2", odometry2)

    cluster1.add(m1)
    cluster2.add(m2)
    cluster1.add(splitted_odom1)
    cluster1.add(splitted_odom3)
    cluster2.add(splitted_odom2)
    cluster2.add(splitted_odom4)

    combinations = [[cluster1, cluster2]]

    result = remove_loops(combinations)
    assert result == combinations

    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()

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
