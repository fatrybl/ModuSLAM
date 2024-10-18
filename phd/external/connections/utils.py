from phd.external.connections.connections_factory import Factory
from phd.external.objects.auxiliary_objects import (
    ClustersWithConnections,
    ClustersWithLeftovers,
    Connection,
)
from phd.external.objects.measurements import (
    ContinuousMeasurement,
    CoreMeasurement,
    FakeMeasurement,
)
from phd.external.objects.measurements_cluster import Cluster
from phd.external.preprocessors.fake_measurement_factory import find_fake_measurement
from phd.external.utils import copy_cluster, create_copy, get_subsequence


def process_single_fake(
    cluster: Cluster, measurement: ContinuousMeasurement, fake_measurement: FakeMeasurement
) -> list[CoreMeasurement]:
    """Processes a connection with the 1-st cluster having a fake measurement.

    Args:
        cluster: cluster to add the new measurement.

        measurement: continuous measurement to be used for connection.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used measurements.
    """
    start = fake_measurement.timestamp
    stop = cluster.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster.add(new_measurement)
    return elements


def process_non_fake(
    connection: Connection, measurement: ContinuousMeasurement
) -> list[CoreMeasurement]:
    """Processes a connection when the 1-st cluster has no fake measurement.

    Args:
        connection: connection to be processed.

        measurement: continuous measurement to be used for connection.

    Returns:
        used elements.
    """
    cluster1 = connection.cluster1
    cluster2 = connection.cluster2
    start = cluster1.timestamp
    stop = cluster2.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    if len(elements) > 0:
        new_measurement = ContinuousMeasurement(elements)
        cluster2.add(new_measurement)

    return elements


def process_fake_and_non_fake(
    connection: Connection,
    measurement: ContinuousMeasurement,
    fake_measurement: FakeMeasurement,
) -> list[CoreMeasurement]:
    """Processes a connection when the 1-st cluster has both fake and real measurements.

    Args:
        connection: connection to be processed.

        measurement: continuous measurement to be used for connection.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used elements.
    """
    used_elements = []
    cluster1 = connection.cluster1
    elements = process_single_fake(cluster1, measurement, fake_measurement)
    cluster1.remove(fake_measurement)
    used_elements += elements

    elements = process_non_fake(connection, measurement)
    used_elements += elements

    return used_elements


def fill_single_connection(
    cluster: Cluster, measurement: ContinuousMeasurement
) -> tuple[Cluster, list[CoreMeasurement]]:
    """Creates a new cluster and adds a continuous measurement to it.

    Args:
        cluster: a cluster to be copied.

        measurement: a continuous measurement to add.

    Returns:
        new cluster and unused measurements.
    """
    cluster_copy = copy_cluster(cluster)
    fake_measurement = find_fake_measurement(cluster_copy.measurements)

    if fake_measurement:
        cluster_copy.remove(fake_measurement)

    start = measurement.time_range.start
    stop = cluster_copy.timestamp
    elements, _, _ = get_subsequence(measurement.elements, start, stop)
    leftovers = [el for el in measurement.elements if el not in elements]
    new_measurement = ContinuousMeasurement(elements)
    cluster_copy.add(new_measurement)
    return cluster_copy, leftovers


def fill_connections(
    item: ClustersWithConnections, measurement: ContinuousMeasurement
) -> tuple[list[Cluster], list[CoreMeasurement]]:
    """Fills connections using the continuous measurement.

    Args:
        item: clusters and connections.

        measurement: a continuous measurement to be used for connections.

    Returns:
        unused discrete measurements.
    """
    used_elements = set[CoreMeasurement]()

    for connection in item.connections:

        measurements = connection.cluster1.measurements[:]
        num_measurements = len(measurements)
        fake_measurement = find_fake_measurement(measurements)

        if fake_measurement and num_measurements == 1:
            elements = process_single_fake(connection.cluster2, measurement, fake_measurement)
            item.clusters.remove(connection.cluster1)

        elif fake_measurement and num_measurements > 1:
            elements = process_fake_and_non_fake(connection, measurement, fake_measurement)

        else:
            elements = process_non_fake(connection, measurement)

        used_elements.update(elements)

    leftovers = [el for el in measurement.elements if el not in used_elements]
    leftovers.sort(key=lambda el: el.timestamp)
    return item.clusters, leftovers


def get_clusters_and_leftovers(
    clusters_combinations: list[list[Cluster]], measurement: ContinuousMeasurement
) -> list[ClustersWithLeftovers]:
    """Creates combinations of clusters and unused measurements.

    Args:
        clusters_combinations: combinations of clusters.

        measurement: a continuous measurement to use elements of.

    Returns:
        combinations of clusters and corresponding unused elements.
    """

    variants: list[ClustersWithLeftovers] = []

    for clusters in clusters_combinations:

        if len(clusters) == 1:
            new_cluster, leftovers = fill_single_connection(clusters[0], measurement)
            v = ClustersWithLeftovers([new_cluster], leftovers)
            variants.append(v)

        else:
            combinations = Factory.create_combinations(clusters)

            for connections in combinations:
                clusters_copy, connections_copy = create_copy(clusters, connections)
                item = ClustersWithConnections(clusters_copy, connections_copy)
                new_clusters, leftovers = fill_connections(item, measurement)
                v = ClustersWithLeftovers(new_clusters, leftovers)
                variants.append(v)

    return variants
