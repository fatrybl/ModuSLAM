import logging
from collections.abc import Iterable, Sequence

from src.bridge.auxiliary_dataclasses import CandidateWithClusters
from src.bridge.candidates_factory import create_graph_elements
from src.external.utils import get_subsequence, group_by_timestamp
from src.external.variants_factory import Factory as VariantsFactory
from src.logger.logging_config import frontend_manager
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.group import MeasurementGroup
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu import ContinuousImu, Imu
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphCandidate
from src.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class Factory:
    """Expands the graph connecting core measurements with IMU sequentially."""

    @staticmethod
    def create_candidate_with_clusters(
        graph: Graph, data: dict[type[Measurement], OrderedSet[Measurement]]
    ) -> CandidateWithClusters:
        """Creates new vertices & edges for the graph using the measurements.

        Args:
            graph: a graph to create new elements for.

            data: a table of measurements to create new edges.

        Returns:
            a list of new graph elements.
        """

        if graph.vertex_storage.clusters:
            latest_cluster = graph.vertex_storage.sorted_clusters[-1]
            latest_t = latest_cluster.time_range.stop
        else:
            latest_t = None

        clusters = Factory._create_clusters_with_leftovers(data, latest_t)

        elements = create_graph_elements(graph, clusters)

        candidate = GraphCandidate(graph, elements, num_unused=0, leftovers=[])

        return CandidateWithClusters(candidate, clusters)

    @classmethod
    def _create_clusters_with_leftovers(
        cls, data: dict[type[Measurement], OrderedSet[Measurement]], left_limit_t: int | None
    ) -> list[MeasurementCluster]:
        """Creates clusters with leftovers from the measurements.

        Args:
            data: a table with measurements.

            left_limit_t: a left limit timestamp.

        Returns:
            clusters with leftovers.
        """

        core_measurements, imu_measurements = VariantsFactory.separate_measurements(data)

        if not core_measurements:
            raise ValueError("No core measurements provided.")

        core_measurements = VariantsFactory.split_and_sort(core_measurements, left_limit_t)

        imu_measurements = sorted(imu_measurements, key=lambda x: x.timestamp)

        groups = group_by_timestamp(core_measurements)

        m_clusters = cls._create_clusters(groups)

        if imu_measurements:
            cls._connect_clusters(m_clusters, imu_measurements)
            cls._process_first_cluster(m_clusters[0], imu_measurements, left_limit_t)

        return m_clusters

    @staticmethod
    def _create_clusters(groups: Iterable[MeasurementGroup]) -> list[MeasurementCluster]:
        """Creates measurement clusters from the groups of measurements.

        Args:
            groups: a list of groups of measurements.

        Returns:
            measurement clusters.
        """
        clusters = []
        for group in groups:
            cluster = MeasurementCluster()

            for item in group.measurements:
                cluster.add(item)

            clusters.append(cluster)

        return clusters

    @staticmethod
    def _connect_clusters(
        clusters: Sequence[MeasurementCluster], imu_measurements: list[Imu]
    ) -> None:
        """Connects clusters with IMU measurements sequentially.

        Args:
            clusters: a list of measurement clusters.

            imu_measurements: a list of IMU measurements.
        """
        num_clusters = len(clusters)
        for i in range(num_clusters - 1):
            cluster1, cluster2 = clusters[i], clusters[i + 1]
            start, stop = cluster1.timestamp, cluster2.timestamp

            subsequence, _, _ = get_subsequence(imu_measurements, start, stop, False)

            if not subsequence:
                logger.warning("No IMU measurements found between clusters.")
                continue

            continuous = ContinuousImu(subsequence, start, stop)

            cluster2.add(continuous)

    @staticmethod
    def _process_first_cluster(
        cluster: MeasurementCluster, imu_measurements: list[Imu], left_limit_t: int | None
    ):
        """Process IMU connection for the 1-st cluster.

        Args:
            cluster: a cluster to process.

            imu_measurements: a list of IMU measurements.

            left_limit_t: a left limit timestamp.
        """
        stop = cluster.timestamp
        first_imu_t = imu_measurements[0].timestamp

        if left_limit_t is None:
            start = first_imu_t
        else:
            start = left_limit_t

        if start < stop:
            subsequence, _, _ = get_subsequence(imu_measurements, start, stop, False)
            continuous = ContinuousImu(subsequence, start, stop)
            cluster.add(continuous)
