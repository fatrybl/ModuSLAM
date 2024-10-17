from phd.external.connections.connections_factory import Factory
from phd.external.objects.auxiliary_objects import (
    ClustersWithConnections,
    ClustersWithLeftovers,
)
from phd.external.objects.measurements import ContinuousMeasurement, CoreMeasurement
from phd.external.objects.measurements_cluster import Cluster
from phd.external.preprocessors.fake_measurement_factory import (
    find_fake_measurement,
    process_fake_and_non_fake,
    process_non_fake,
    process_single_fake,
)
from phd.external.utils import copy_cluster, create_copy, get_subsequence


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


def fill_multiple_connections(
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
            elements, empty_cluster = process_single_fake(connection, measurement, fake_measurement)
            item.clusters.remove(empty_cluster)

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
            # TODO: filter irrealizable combinations due to limitations.

            for connections in combinations:
                clusters_copy, connections_copy = create_copy(clusters, connections)
                item = ClustersWithConnections(clusters_copy, connections_copy)
                new_clusters, leftovers = fill_multiple_connections(item, measurement)
                v = ClustersWithLeftovers(new_clusters, leftovers)
                variants.append(v)

    return variants
