from bisect import bisect_left
from collections.abc import Iterable
from typing import TypeVar, cast

from phd.external.connections_factory import Factory
from phd.external.objects.auxiliary_objects import (
    ClustersWithConnections,
    ClustersWithLeftovers,
    Connection,
)
from phd.external.objects.cluster import MeasurementsCluster
from phd.external.objects.measurements import (
    ContinuousMeasurement,
    CoreMeasurement,
    FakeMeasurement,
    Measurement,
)

T = TypeVar("T", bound=Measurement)


def get_subsequence(sequence: list[T], start: int, stop: int) -> tuple[list[T], int, int]:
    """Gets the sub-sequence of items  within the given range.

    Args:
        sequence: a sequence of items to get a sub-sequence from.

        start: left timestamp limit (inclusive).

        stop: right timestamp limit (exclusive).

    Returns:
        a subsequence of the given range, start index, stop index.
    """
    if not sequence or start >= stop:
        raise ValueError("Empty sequence or invalid limits.")

    timestamps: list[int] = [item.timestamp for item in sequence]
    start_idx = bisect_left(timestamps, start)
    stop_idx = bisect_left(timestamps, stop)

    return sequence[start_idx:stop_idx], start_idx, stop_idx


def find_fake_measurement(measurements: Iterable[Measurement]) -> FakeMeasurement | None:
    """Finds the 1-st fake measurement in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        the 1-st fake measurement in the sequence of measurements or None if not found.
    """
    for m in measurements:
        if m.value == FakeMeasurement.fake_value:
            m = cast(FakeMeasurement, m)
            return m
    return None


def process_single_fake(
    connection: Connection,
    measurement: ContinuousMeasurement,
    fake_measurement: FakeMeasurement,
):
    """Processes a connection with the 1-st cluster having a fake measurement.

    Args:
        connection: connection to be processed.

        measurement: continuous measurement to be used for connection.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used measurements and empty cluster.
    """
    cluster1 = connection.cluster1
    cluster2 = connection.cluster2
    start = fake_measurement.timestamp
    stop = cluster2.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster2.add(new_measurement)
    return elements, cluster1


def process_fake_and_non_fake(
    connection: Connection,
    measurement: ContinuousMeasurement,
    fake_measurement: FakeMeasurement,
):
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
    cluster2 = connection.cluster2
    start = fake_measurement.timestamp
    stop = cluster1.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster1.add(new_measurement)
    cluster1.remove(fake_measurement)
    used_elements += elements

    start = cluster1.timestamp
    stop = cluster2.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster2.add(new_measurement)
    used_elements += elements
    return used_elements


def process_non_fake(connection: Connection, measurement: ContinuousMeasurement):
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
    new_measurement = ContinuousMeasurement(elements)
    cluster2.add(new_measurement)
    return elements


def fill_single_connection(
    cluster: MeasurementsCluster, measurement: ContinuousMeasurement
) -> tuple[MeasurementsCluster, list[CoreMeasurement]]:
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
) -> tuple[list[MeasurementsCluster], list[CoreMeasurement]]:
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
    clusters_combinations: list[list[MeasurementsCluster]], measurement: ContinuousMeasurement
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
            # TODO: filter irrealizable combinations here due to limitations.

            for connections in combinations:
                clusters_copy, connections_copy = create_copy(clusters, connections)
                item = ClustersWithConnections(clusters_copy, connections_copy)
                new_clusters, leftovers = fill_multiple_connections(item, measurement)
                v = ClustersWithLeftovers(new_clusters, leftovers)
                variants.append(v)

    return variants


def copy_cluster(cluster: MeasurementsCluster) -> MeasurementsCluster:
    """Creates a cluster with the same measurements as in the given cluster.

    Args:
        cluster: cluster to copy measurements from.

    Returns:
        new cluster with the same measurements.
    """
    new_cluster = MeasurementsCluster()
    for m in cluster.measurements:
        new_cluster.add(m)
    return new_cluster


def create_copy(
    clusters: list[MeasurementsCluster], connections: list[Connection]
) -> tuple[list[MeasurementsCluster], list[Connection]]:
    """Copies clusters and connections.

    Args:
        clusters: clusters to copy.

        connections: connections to copy.

    Returns:
        clusters and connections with the same values.
    """
    connections_copy = []
    clusters_copy = [copy_cluster(c) for c in clusters]
    cluster_mapping = {original: copy for original, copy in zip(clusters, clusters_copy)}

    for connection in connections:
        cluster1_copy = cluster_mapping[connection.cluster1]
        cluster2_copy = cluster_mapping[connection.cluster2]

        new_con = Connection(cluster1_copy, cluster2_copy)
        connections_copy.append(new_con)

    return clusters_copy, connections_copy


def remove_duplicates(
    clusters_with_leftovers_list: list[ClustersWithLeftovers],
) -> list[ClustersWithLeftovers]:
    """Remove duplicate clusters with leftovers.
    Duplicate: clusters with the same measurements and the same leftovers.

    Args:
        clusters_with_leftovers_list: clusters with leftovers.

    Returns:
        unique clusters with leftovers.
    """
    seen = set()
    unique_clusters_with_leftovers = []

    for clusters_with_leftovers in clusters_with_leftovers_list:

        leftovers = tuple(clusters_with_leftovers.leftovers)

        measurements_list = []
        for cluster in clusters_with_leftovers.clusters:
            current_measurements: list[CoreMeasurement] = []

            for m in cluster.measurements:
                if isinstance(m, ContinuousMeasurement):
                    current_measurements += m.elements
                elif isinstance(m, CoreMeasurement):
                    current_measurements.append(m)

            measurements_list.append(tuple(current_measurements))

        measurements = tuple(measurements_list)
        key = (measurements, leftovers)

        if key not in seen:
            seen.add(key)
            unique_clusters_with_leftovers.append(clusters_with_leftovers)

    return unique_clusters_with_leftovers
