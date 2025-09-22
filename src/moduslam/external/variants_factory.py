from moduslam.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from moduslam.bridge.preprocessors.pose_odometry import split_odometry
from moduslam.external.combinations_factory import Factory as CombinationFactory
from moduslam.external.connections.utils import create_and_fill_connections
from moduslam.external.utils import group_by_timestamp, remove_duplicates, remove_loops
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.base import Measurement
from moduslam.measurement_storage.measurements.imu import Imu
from moduslam.utils.ordered_set import OrderedSet


class Factory:
    """Creates all valid combinations of measurements."""

    @classmethod
    def create(
        cls, data: dict[type[Measurement], OrderedSet[Measurement]], left_limit_t: int | None
    ) -> list[ClustersWithLeftovers]:
        """Creates combinations of clusters with leftover measurements.

        Args:
            data: a table of typed Ordered Sets with measurements.

            left_limit_t: a timestamp of the left limit.

        Returns:
            combinations of clusters with leftover measurements.

        TODO: remove sorting imu measurements ?
        """
        core_measurements, imu_measurements = cls.separate_measurements(data)

        if not core_measurements:
            return []

        core_measurements = cls.split_and_sort(core_measurements, left_limit_t)
        start = core_measurements[0].timestamp
        stop = core_measurements[-1].timestamp

        imu_measurements = sorted(imu_measurements, key=lambda x: x.timestamp)

        groups = group_by_timestamp(core_measurements)

        combinations = CombinationFactory.combine(groups)
        combinations = remove_loops(combinations)

        items = cls._fill_combinations(combinations, imu_measurements, start, stop, left_limit_t)
        return items

    @staticmethod
    def separate_measurements(
        data: dict[type[Measurement], OrderedSet[Measurement]],
    ) -> tuple[list[Measurement], list[Imu]]:
        """Splits data into core and IMU measurements.

        Args:
            data: a dictionary with measurements.

        Returns:
            Non-IMU and IMU measurements.
        """
        imu_measurements: list[Imu] = []
        core_measurements: list[Measurement] = []

        for m_type, m_set in data.items():
            if issubclass(m_type, Imu):
                imu_measurements.extend(m_set.items)
            else:
                core_measurements.extend(m_set.items)

        return core_measurements, imu_measurements

    @staticmethod
    def split_and_sort(measurements: list[Measurement], start: int | None) -> list[Measurement]:
        """Splits and sorts measurements by timestamps.

        Args:
            measurements: list of measurements.

            start: a start timestamp.

        Returns:
            sorted and split measurements.
        """
        measurements = split_odometry(measurements, start)
        measurements.sort(key=lambda x: x.timestamp)
        return measurements

    @staticmethod
    def _fill_combinations(
        core_combinations: list[list[MeasurementCluster]],
        measurements: list[Imu],
        first_core_t: int,
        last_core_t: int,
        left_limit_t: int | None,
    ) -> list[ClustersWithLeftovers]:
        """Combines clusters` combinations with imu measurements (if available).

        Args:
            core_combinations: combinations of clusters with core measurements.

            measurements: IMU measurements.

            first_core_t: a timestamp of the 1-st core measurement.

            last_core_t: a timestamp of the last core measurement.

            left_limit_t: a timestamp of the left limit.

        Returns:
            combinations with leftover imu measurements.
        """
        if not measurements:
            combinations = Factory._create_cluster_with_leftovers(core_combinations)

        else:
            first_imu_t = measurements[0].timestamp

            if first_imu_t >= last_core_t:
                combinations = Factory._create_cluster_with_leftovers(
                    core_combinations, measurements
                )

            else:
                combinations = Factory._combine_with_continuous(
                    core_combinations, measurements, first_core_t, left_limit_t
                )

        return combinations

    @staticmethod
    def _create_cluster_with_leftovers(
        combinations: list[list[MeasurementCluster]],
        measurements: list[Imu] | None = None,
    ) -> list[ClustersWithLeftovers]:
        """Creates clusters with leftover measurements.

        Args:
            combinations: combinations of clusters.

            measurements: IMU measurements.

        Returns:
            clusters with leftover measurements.
        """

        items: list[ClustersWithLeftovers] = []

        for comb in combinations:
            if comb:
                leftovers = measurements if measurements else []
                items.append(ClustersWithLeftovers(comb, leftovers))

        return items

    @staticmethod
    def _combine_with_continuous(
        combinations: list[list[MeasurementCluster]],
        measurements: list[Imu],
        first_core_t: int,
        left_limit_t: int | None,
    ) -> list[ClustersWithLeftovers]:
        """Processes continuous measurements.

        Args:
            combinations: combinations of clusters.

            measurements: discrete IMU measurements.

            first_core_t: a timestamp of the 1-st core measurement.

            left_limit_t: a timestamp of the left limit.

        Returns:
            clusters with unused measurements.
        """

        clusters_with_leftovers = create_and_fill_connections(
            combinations, measurements, first_core_t, left_limit_t
        )
        clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)
        return clusters_with_leftovers
