from phd.external.utils import remove_loops
from phd.measurements.auxiliary_classes import PseudoMeasurement, SplitPoseOdometry
from phd.measurements.cluster import Cluster
from phd.measurements.processed import PoseOdometry
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class TestRemoveLoops:
    identity3 = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    identity4 = (
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )

    def test_remove_loops_with_empty_list(self):
        empty_combinations: list[list[Cluster]] = []
        result = remove_loops(empty_combinations)
        assert result == []

    def test_remove_loops_with_no_loops(self):
        odometry = PoseOdometry(
            1, TimeRange(0, 1), self.identity4, self.identity3, self.identity3, []
        )
        t1 = odometry.time_range.start
        t2 = odometry.time_range.stop
        split_odom1 = SplitPoseOdometry(t1, odometry)
        split_odom2 = SplitPoseOdometry(t2, odometry)
        cluster1, cluster2 = Cluster(), Cluster()
        cluster1.add(split_odom1)
        cluster2.add(split_odom2)
        combinations = [[cluster1, cluster2]]

        result = remove_loops(combinations)
        assert result == combinations

    def test_remove_loops_with_all_loops(self):
        odometry1 = PoseOdometry(
            2, TimeRange(1, 2), self.identity4, self.identity3, self.identity3, []
        )
        odometry2 = PoseOdometry(
            4, TimeRange(3, 4), self.identity4, self.identity3, self.identity3, []
        )
        splitted_odom1 = SplitPoseOdometry(1, odometry1)
        splitted_odom2 = SplitPoseOdometry(2, odometry1)
        splitted_odom3 = SplitPoseOdometry(3, odometry2)
        splitted_odom4 = SplitPoseOdometry(4, odometry2)
        cluster1, cluster2 = Cluster(), Cluster()
        cluster1.add(splitted_odom1)
        cluster1.add(splitted_odom2)  # Loop in cluster1
        cluster2.add(splitted_odom3)
        cluster2.add(splitted_odom4)  # Loop in cluster2
        combinations = [[cluster1], [cluster2]]

        result = remove_loops(combinations)
        assert result == []

    def test_remove_loops_with_mixed_combinations(self):
        odometry1 = PoseOdometry(
            2, TimeRange(1, 2), self.identity4, self.identity3, self.identity3, []
        )
        odometry2 = PoseOdometry(
            4, TimeRange(3, 4), self.identity4, self.identity3, self.identity3, []
        )
        odometry3 = PoseOdometry(
            6, TimeRange(5, 6), self.identity4, self.identity3, self.identity3, []
        )
        splitted_odom1 = SplitPoseOdometry(1, odometry1)
        splitted_odom2 = SplitPoseOdometry(2, odometry1)
        splitted_odom3 = SplitPoseOdometry(3, odometry2)
        splitted_odom4 = SplitPoseOdometry(4, odometry2)
        splitted_odom5 = SplitPoseOdometry(5, odometry3)
        splitted_odom6 = SplitPoseOdometry(6, odometry3)
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

    def test_remove_loops_with_single_cluster_with_loops(self):
        odometry = PoseOdometry(
            2, TimeRange(1, 2), self.identity4, self.identity3, self.identity3, []
        )
        splitted_odom1 = SplitPoseOdometry(1, odometry)
        splitted_odom2 = SplitPoseOdometry(2, odometry)  # Loop
        cluster = Cluster()
        cluster.add(splitted_odom1)
        cluster.add(splitted_odom2)
        combinations = [[cluster]]

        result = remove_loops(combinations)
        assert result == []

    def test_remove_loops_with_no_splitted_odometry(self):
        cluster1, cluster2 = Cluster(), Cluster()
        m1 = PseudoMeasurement(1, "value1")
        m2 = PseudoMeasurement(2, "value2")
        cluster1.add(m1)
        cluster2.add(m2)
        combinations = [[cluster1, cluster2]]

        result = remove_loops(combinations)
        assert result == combinations

    def test_remove_loops_all_clusters_without_loops(self):
        cluster1, cluster2 = Cluster(), Cluster()
        m1, m2 = PseudoMeasurement(1, "value1"), PseudoMeasurement(2, "value2")
        odometry1 = PoseOdometry(
            2, TimeRange(1, 2), self.identity4, self.identity3, self.identity3, []
        )
        odometry2 = PoseOdometry(
            4, TimeRange(3, 4), self.identity4, self.identity3, self.identity3, []
        )
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
