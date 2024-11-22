from phd.bridge.objects.auxiliary_classes import MeasurementGroup
from phd.bridge.objects.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.objects.measurements_cluster import Cluster
from phd.bridge.preprocessors.fake_measurement_factory import add_fake_cluster
from phd.bridge.preprocessors.pose_odometry import find_and_replace
from phd.external.combinations_factory import Factory as CombinationFactory
from phd.external.connections.utils import get_clusters_and_leftovers
from phd.external.utils import group_by_timestamp, remove_duplicates, remove_loops
from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import Imu, Measurement
from phd.moduslam.utils.ordered_set import OrderedSet


class Factory:
    """Creates all valid combinations of measurements."""

    @classmethod
    def create(
        cls, storage: MeasurementStorage
    ) -> list[ClustersWithLeftovers] | list[list[Cluster]]:
        """Creates combinations of clusters w or w/o leftover measurements.

        Args:
            storage: a storage with measurements.

        Returns:
            combinations of clusters w or w/o leftover measurements.
        """

        other_measurements, imu_measurements = cls._separate_measurements(storage.data)

        groups = cls._prepare_measurements(other_measurements)
        combinations = CombinationFactory.combine(groups)
        combinations = remove_loops(combinations)

        if imu_measurements:
            start = imu_measurements[0].timestamp
            for combination in combinations:
                add_fake_cluster(combination, start)

            combs_with_leftovers = cls._combine_with_continuous(combinations, imu_measurements)
            return combs_with_leftovers

        else:
            return combinations

    @staticmethod
    def _separate_measurements(
        data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> tuple[list[Measurement], list[Measurement]]:
        """Splits data into IMU measurements and others.

        Args:
            data: a dictionary with measurements.

        Returns:
            Non-IMU and IMU measurements.
        """
        imu_measurements: list[Measurement] = []
        other_measurements: list[Measurement] = []

        for m_type, m_set in data.items():
            if m_type == Imu:
                imu_measurements.extend(m_set.items)
            else:
                other_measurements.extend(m_set.items)

        return other_measurements, imu_measurements

    @staticmethod
    def _prepare_measurements(measurements: list[Measurement]) -> list[MeasurementGroup]:
        """Prepares measurements for further processing.

        Args:
            measurements: different measurements.

        Returns:
            groups of measurements.
        """
        measurements = find_and_replace(measurements)
        measurements.sort(key=lambda x: x.timestamp)
        groups = group_by_timestamp(measurements)
        return groups

    @staticmethod
    def _combine_with_continuous(
        combinations: list[list[Cluster]], measurements: list[Measurement]
    ) -> list[ClustersWithLeftovers]:
        """Processes continuous measurements.

        Args:
            combinations: combinations of clusters.

            measurements: continuous measurements.

        Returns:
            clusters with unused measurements.
        """

        clusters_with_leftovers = get_clusters_and_leftovers(combinations, measurements)
        clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)
        return clusters_with_leftovers


# if __name__ == "__main__":

# identity3 = (
#     (1, 0, 0),
#     (0, 1, 0),
#     (0, 0, 1),
# )
# identity4 = (
#     (1, 0, 0, 0),
#     (0, 1, 0, 0),
#     (0, 0, 1, 0),
#     (0, 0, 0, 1),
# )
#
# d1 = PseudoMeasurement(1, "a")
# d2 = PseudoMeasurement(3, "b")
# # d3 = CoreMeasurement(5, "c")
# # d4 = CoreMeasurement(7, "d")
# imu1 = PseudoMeasurement(0, 0.5)
# imu2 = PseudoMeasurement(1, 0.5)
# imu3 = PseudoMeasurement(2, 0.5)
# # imu4 = CoreMeasurement(4, 0.5)
# # imu5 = CoreMeasurement(5, 0.5)
# # imu6 = DiscreteMeasurement(6, 0.5)
# imu_readings: list[Measurement] = [imu1, imu2, imu3]
# odom1 = PoseOdometry(1, TimeRange(0, 1), identity4, identity3, identity3, [])
# odom2 = PoseOdometry(2, TimeRange(1, 2), identity4, identity3, identity3, [])
#
# measurements: list[Measurement] = [d1, d2, odom1, odom2]
#
# # ===============================================================================================
#
# split_odometry_measurements = find_and_split(measurements)
# if split_odometry_measurements:
#     measurements = remove_odometry(measurements)
#     measurements += split_odometry_measurements
#
# measurements.sort(key=lambda m: m.timestamp)
#
# if imu_readings:
#     add_fake_measurement(measurements, imu_readings)
#
# groups = group_by_timestamp(measurements)
#
# clusters_combinations = CombinationFactory.combine(groups)
# clusters_combinations = remove_loops(clusters_combinations)
#
# if imu_readings:
#     clusters_with_leftovers = get_clusters_and_leftovers(clusters_combinations, imu_readings)
#
#     clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)
#
#     for item in clusters_with_leftovers:
#         print(item)
#
# else:
#     for comb in clusters_combinations:
#         print(comb)
