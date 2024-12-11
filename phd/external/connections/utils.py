from typing import cast

from phd.bridge.auxiliary_dataclasses import (
    ClustersWithConnections,
    ClustersWithLeftovers,
)
from phd.external.connections.connections_factory import Factory
from phd.external.utils import copy_cluster, create_copy, get_subsequence
from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.imu import ContinuousImu, Imu


def fill_one_connection_with_imu(
    cluster: MeasurementCluster, measurements: list[Imu]
) -> tuple[MeasurementCluster, list[Imu]]:
    """Creates a new cluster and adds a continuous measurement to it.

    Args:
        cluster: a cluster to be copied.

        measurements: discrete IMU measurements to fill in the connections.

    Returns:
        new cluster and unused measurements.
    """
    cluster_copy = copy_cluster(cluster)

    start = measurements[0].timestamp
    stop = cluster_copy.timestamp
    subsequence, _, _ = get_subsequence(measurements, start, stop)
    subsequence_set = set(subsequence)
    leftovers = [m for m in measurements if m not in subsequence_set]
    new_measurement = ContinuousImu(subsequence, start, stop)
    cluster_copy.add(new_measurement)
    return cluster_copy, leftovers


def fill_connections_with_imu(
    item: ClustersWithConnections, measurements: list[Imu]
) -> tuple[list[MeasurementCluster], list[Imu]]:
    """Replaces virtual connections with continuous IMU measurements.

    Args:
        item: clusters and connections.

        measurements: discrete IMU measurements to create continuous IMU measurements.

    Returns:
        clusters and unused discrete IMU measurements.
    """
    used_measurements = set[Measurement]()

    for connection in item.connections:

        start = connection.cluster1.timestamp
        stop = connection.cluster2.timestamp
        subsequence, _, _ = get_subsequence(measurements, start, stop)
        m = ContinuousImu(subsequence, start, stop)
        connection.cluster2.add(m)

        used_measurements.update(subsequence)

        if connection.cluster1.fake_measurements:
            item.clusters.remove(connection.cluster1)

    leftovers = [m for m in measurements if m not in used_measurements]
    leftovers.sort(key=lambda el: el.timestamp)
    return item.clusters, leftovers


def get_clusters_and_leftovers(
    clusters_combinations: list[list[MeasurementCluster]], measurements: list[Imu]
) -> list[ClustersWithLeftovers]:
    """Creates combinations of clusters and unused measurements.

    Args:
        clusters_combinations: combinations of clusters.

        measurements: IMU measurements to fill in the connections.

    Returns:
        combinations of clusters with corresponding unused elements.
    """
    variants: list[ClustersWithLeftovers] = []

    for clusters in clusters_combinations:

        if len(clusters) == 1:
            new_cluster, imu_leftovers = fill_one_connection_with_imu(clusters[0], measurements)
            leftovers = cast(list[Measurement], imu_leftovers)
            v = ClustersWithLeftovers([new_cluster], leftovers)
            variants.append(v)

        else:
            combinations = Factory.create_combinations(clusters)

            for connections in combinations:
                clusters_copy, connections_copy = create_copy(clusters, connections)
                item = ClustersWithConnections(clusters_copy, connections_copy)
                new_clusters, imu_leftovers = fill_connections_with_imu(item, measurements)
                leftovers = cast(list[Measurement], imu_leftovers)
                v = ClustersWithLeftovers(new_clusters, leftovers)
                variants.append(v)

    return variants
