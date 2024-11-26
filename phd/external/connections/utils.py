from typing import cast

from phd.bridge.objects.auxiliary_dataclasses import (
    ClustersWithConnections,
    ClustersWithLeftovers,
)
from phd.bridge.objects.measurements_cluster import Cluster
from phd.external.connections.connections_factory import Factory
from phd.external.utils import copy_cluster, create_copy, get_subsequence
from phd.measurements.processed_measurements import (
    ContinuousImuMeasurement,
    ContinuousMeasurement,
    Imu,
    Measurement,
)


def fill_single_connection(
    cluster: Cluster, measurements: list[Measurement]
) -> tuple[Cluster, list[Measurement]]:
    """Creates a new cluster and adds a continuous measurement to it.

    Args:
        cluster: a cluster to be copied.

        measurements: measurements to fill in the connections.

    Returns:
        new cluster and unused measurements.
    """
    cluster_copy = copy_cluster(cluster)

    start = measurements[0].timestamp
    stop = cluster_copy.timestamp
    subsequence, _, _ = get_subsequence(measurements, start, stop)
    subsequence_set = set(subsequence)
    leftovers = [m for m in measurements if m not in subsequence_set]
    new_measurement = ContinuousMeasurement(subsequence)
    cluster_copy.add(new_measurement)
    return cluster_copy, leftovers


def fill_connections(
    item: ClustersWithConnections, measurements: list[Measurement]
) -> tuple[list[Cluster], list[Measurement]]:
    """Creates new measurements to replace the connections using the  given
    measurements.

    Args:
        item: clusters and connections.

        measurements: measurements to replace the connections.

    Returns:
        clusters and unused measurements.

    TODO: remove type cast.
    """
    used_measurements = set[Measurement]()

    for connection in item.connections:

        start = connection.cluster1.timestamp
        stop = connection.cluster2.timestamp
        subsequence, _, _ = get_subsequence(measurements, start, stop)
        imu_subsequence = cast(list[Imu], subsequence)
        m = ContinuousImuMeasurement(imu_subsequence, stop)
        connection.cluster2.add(m)

        used_measurements.update(subsequence)

        if connection.cluster1.fake_measurements:
            item.clusters.remove(connection.cluster1)

    leftovers = [m for m in measurements if m not in used_measurements]
    leftovers.sort(key=lambda el: el.timestamp)
    return item.clusters, leftovers


def get_clusters_and_leftovers(
    clusters_combinations: list[list[Cluster]], measurements: list[Measurement]
) -> list[ClustersWithLeftovers]:
    """Creates combinations of clusters and unused measurements.

    Args:
        clusters_combinations: combinations of clusters.

        measurements: measurements to fill in the connections.

    Returns:
        combinations of clusters with corresponding unused elements.
    """

    variants: list[ClustersWithLeftovers] = []

    for clusters in clusters_combinations:

        if len(clusters) == 1:
            new_cluster, leftovers = fill_single_connection(clusters[0], measurements)
            v = ClustersWithLeftovers([new_cluster], leftovers)
            variants.append(v)

        else:
            combinations = Factory.create_combinations(clusters)

            for connections in combinations:
                clusters_copy, connections_copy = create_copy(clusters, connections)
                item = ClustersWithConnections(clusters_copy, connections_copy)
                new_clusters, leftovers = fill_connections(item, measurements)
                v = ClustersWithLeftovers(new_clusters, leftovers)
                variants.append(v)

    return variants
