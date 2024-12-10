from phd.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.preprocessors.fake_measurement_factory import add_fake_cluster
from phd.bridge.preprocessors.pose_odometry import find_and_replace
from phd.external.combinations_factory import Factory as CombinationFactory
from phd.external.connections.utils import get_clusters_and_leftovers
from phd.external.utils import group_by_timestamp, remove_duplicates, remove_loops
from phd.measurement_storage.cluster import Cluster
from phd.measurement_storage.measurement_group import Group
from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.imu import Imu
from phd.measurement_storage.storage import MeasurementStorage
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

        core_measurements, imu_measurements = cls._separate_measurements(storage.data)
        groups = cls._prepare_measurements(core_measurements)
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
            if m_type == Imu:
                imu_measurements.extend(m_set.items)
            else:
                core_measurements.extend(m_set.items)

        return core_measurements, imu_measurements

    @staticmethod
    def _prepare_measurements(measurements: list[Measurement]) -> list[Group]:
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
        combinations: list[list[Cluster]], measurements: list[Imu]
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
