from phd.bridge.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.preprocessors.fake_measurement_factory import add_fake_cluster
from phd.bridge.preprocessors.pose_odometry import split_odometry
from phd.external.combinations_factory import Factory as CombinationFactory
from phd.external.connections.utils import get_clusters_and_leftovers
from phd.external.utils import group_by_timestamp, remove_duplicates, remove_loops
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.imu import Imu
from phd.utils.ordered_set import OrderedSet


class Factory:
    """Creates all valid combinations of measurements."""

    @classmethod
    def create(
        cls, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> list[ClustersWithLeftovers] | list[list[MeasurementCluster]]:
        """Creates combinations of clusters w or w/o leftover measurements.

        Args:
            data: table of typed Ordered Sets with measurements.

        Returns:
            combinations of clusters w or w/o leftover measurements.

        TODO: add tests !!!.
        """
        core_measurements, imu_measurements = cls._separate_measurements(data)
        core_measurements = cls._prepare_measurements(core_measurements)
        groups = group_by_timestamp(core_measurements)

        combinations = CombinationFactory.combine(groups)
        combinations = remove_loops(combinations)

        if imu_measurements:
            first_imu_t = imu_measurements[0].timestamp
            first_core_t = core_measurements[0].timestamp

            if first_imu_t < first_core_t:
                for combination in combinations:
                    add_fake_cluster(combination, first_imu_t)

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
            if issubclass(m_type, Imu):
                imu_measurements.extend(m_set.items)
            else:
                core_measurements.extend(m_set.items)

        return core_measurements, imu_measurements

    @staticmethod
    def _prepare_measurements(measurements: list[Measurement]) -> list[Measurement]:
        """Prepares measurements for further processing.

        Args:
            measurements: different measurements.

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
