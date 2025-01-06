from typing import cast

from src.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from src.bridge.preprocessors.fake_measurement_factory import add_fake_cluster
from src.bridge.preprocessors.pose_odometry import split_odometry
from src.external.combinations_factory import Factory as CombinationFactory
from src.external.connections.utils import get_clusters_and_leftovers
from src.external.utils import group_by_timestamp, remove_duplicates, remove_loops
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import Imu
from src.utils.ordered_set import OrderedSet


class Factory:
    """Creates all valid combinations of measurements."""

    @classmethod
    def create(
        cls, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> list[ClustersWithLeftovers]:
        """Creates combinations of clusters with leftover measurements.

        Args:
            data: table of typed Ordered Sets with measurements.

        Returns:
            combinations of clusters with leftover measurements.
        """
        core_measurements, imu_measurements = cls._separate_measurements(data)

        if not core_measurements:
            return []

        core_measurements = cls._split_and_sort(core_measurements)
        imu_measurements = sorted(imu_measurements, key=lambda x: x.timestamp)

        groups = group_by_timestamp(core_measurements)

        core_combinations = CombinationFactory.combine(groups)
        core_combinations = remove_loops(core_combinations)

        start = core_measurements[0].timestamp
        stop = core_measurements[-1].timestamp

        items = cls._fill_combinations(core_combinations, imu_measurements, start, stop)

        return items

    @staticmethod
    def _fill_combinations(
        core_combinations: list[list[MeasurementCluster]],
        imu_measurements: list[Imu],
        start: int,
        stop: int,
    ) -> list[ClustersWithLeftovers]:
        """Combines clusters` combinations with imu measurements (if available).

        Args:
            core_combinations: combinations of clusters with core measurements.

            imu_measurements: IMU measurements.

            start: start timestamp.

            stop: stop timestamp.

        Returns:
            combinations with leftover imu measurements (if available).
        """
        if not imu_measurements:
            combinations = Factory._create_cluster_with_leftovers(core_combinations)

        else:
            first_imu_t = imu_measurements[0].timestamp

            if first_imu_t < start:
                for comb in core_combinations:
                    add_fake_cluster(comb, first_imu_t)

            if first_imu_t >= stop:
                combinations = Factory._create_cluster_with_leftovers(
                    core_combinations, imu_measurements
                )
            else:
                combinations = Factory._combine_with_continuous(core_combinations, imu_measurements)

        return combinations

    @staticmethod
    def _create_cluster_with_leftovers(
        combinations: list[list[MeasurementCluster]],
        imu_measurements: list[Imu] | None = None,
    ) -> list[ClustersWithLeftovers]:
        """Creates clusters with leftover measurements.

        Args:
            combinations: combinations of clusters.

            imu_measurements: IMU measurements.

        Returns:
            clusters with leftover measurements.
        """

        items: list[ClustersWithLeftovers] = []

        for comb in combinations:
            if comb:
                if imu_measurements:
                    leftovers = cast(list[Measurement], imu_measurements)  # avoid MyPy error
                else:
                    leftovers = []

                items.append(ClustersWithLeftovers(comb, leftovers))

        return items

    @staticmethod
    def _separate_measurements(
        data: dict[type[Measurement], OrderedSet[Measurement]]
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
    def _split_and_sort(measurements: list[Measurement]) -> list[Measurement]:
        """Splits and sorts measurements by timestamps.

        Args:
            measurements: list of measurements.

        Returns:
            sorted and split measurements.
        """
        measurements = split_odometry(measurements)
        measurements.sort(key=lambda x: x.timestamp)
        return measurements

    @staticmethod
    def _combine_with_continuous(
        combinations: list[list[MeasurementCluster]], measurements: list[Imu]
    ) -> list[ClustersWithLeftovers]:
        """Processes continuous measurements.

        Args:
            combinations: combinations of clusters.

            measurements: discrete IMU measurements.

        Returns:
            clusters with unused measurements.
        """

        clusters_with_leftovers = get_clusters_and_leftovers(combinations, measurements)
        clusters_with_leftovers = remove_duplicates(clusters_with_leftovers)
        return clusters_with_leftovers
