from phd.bridge.objects.auxiliary_classes import FakeMeasurement
from phd.bridge.objects.auxiliary_dataclasses import (
    ClustersWithConnections,
    ClustersWithLeftovers,
    Connection,
)
from phd.bridge.objects.measurements_cluster import Cluster
from phd.bridge.preprocessors.fake_measurement_factory import find_fake_measurement
from phd.external.connections.connections_factory import Factory
from phd.external.utils import copy_cluster, create_copy, get_subsequence
from phd.measurements.processed_measurements import ContinuousMeasurement, Measurement


def process_single_fake(
    cluster: Cluster, measurements: list[Measurement], fake_measurement: FakeMeasurement
) -> list[Measurement]:
    """Processes a connection with the 1-st cluster having a fake measurement.

    Args:
        cluster: cluster to add the new measurement.

        measurements: measurements to fill in the connections.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used measurements.
    """
    start = fake_measurement.timestamp
    stop = cluster.timestamp
    subsequence, _, stop = get_subsequence(measurements, start, stop)
    new_measurement = ContinuousMeasurement(subsequence)
    cluster.add(new_measurement)
    return subsequence


def process_non_fake(connection: Connection, measurements: list[Measurement]) -> list[Measurement]:
    """Processes a connection when the 1-st cluster has no fake measurement.

    Args:
        connection: connection to be processed.

        measurements: measurements to fill in the connections.

    Returns:
        used elements.
    """
    cluster1 = connection.cluster1
    cluster2 = connection.cluster2
    start = cluster1.timestamp
    stop = cluster2.timestamp
    subsequence, _, stop = get_subsequence(measurements, start, stop)
    if len(measurements) > 0:
        new_measurement = ContinuousMeasurement(subsequence)
        cluster2.add(new_measurement)

    return subsequence


def process_fake_and_non_fake(
    connection: Connection,
    measurements: list[Measurement],
    fake_measurement: FakeMeasurement,
) -> list[Measurement]:
    """Processes a connection when the 1-st cluster has both fake and real measurements.

    Args:
        connection: connection to be processed.

        measurements: measurements to fill in the connections.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used elements.
    """
    used_measurements = []
    cluster1 = connection.cluster1
    subsequence = process_single_fake(cluster1, measurements, fake_measurement)
    cluster1.remove(fake_measurement)
    used_measurements += subsequence

    subsequence = process_non_fake(connection, measurements)
    used_measurements += subsequence

    return used_measurements


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
    fake_measurement = find_fake_measurement(cluster_copy.measurements)

    if fake_measurement:
        cluster_copy.remove(fake_measurement)

    start = measurements[0].timestamp
    stop = cluster_copy.timestamp
    subsequence, _, _ = get_subsequence(measurements, start, stop)
    leftovers = [m for m in measurements if m not in subsequence]
    new_measurement = ContinuousMeasurement(subsequence)
    cluster_copy.add(new_measurement)
    return cluster_copy, leftovers


def fill_connections(
    item: ClustersWithConnections, measurements: list[Measurement]
) -> tuple[list[Cluster], list[Measurement]]:
    """Fills connections using the measurements.

    Args:
        item: clusters and connections.

        measurements: measurements to fill in the connections.

    Returns:
        unused measurements.
    """
    all_used_measurements = set[Measurement]()

    for connection in item.connections:

        cluster1_measurements = connection.cluster1.measurements[:]
        num_measurements = len(cluster1_measurements)
        fake_measurement = find_fake_measurement(cluster1_measurements)

        if fake_measurement and num_measurements == 1:
            used_measurements = process_single_fake(
                connection.cluster2, measurements, fake_measurement
            )
            item.clusters.remove(connection.cluster1)

        elif fake_measurement and num_measurements > 1:
            used_measurements = process_fake_and_non_fake(
                connection, measurements, fake_measurement
            )

        else:
            used_measurements = process_non_fake(connection, measurements)

        all_used_measurements.update(used_measurements)

    leftovers = [m for m in measurements if m not in all_used_measurements]
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
        combinations of clusters and corresponding unused elements.
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
