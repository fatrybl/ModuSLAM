from bisect import bisect_left
from copy import deepcopy
from typing import TypeVar

from phd_thesis.src.connections import ConnectionsFactory
from phd_thesis.src.objects.auxiliary_objects import (
    ClustersWithConnections,
    ClustersWithLeftovers,
)
from phd_thesis.src.objects.cluster import Cluster
from phd_thesis.src.objects.measurements import (
    ContinuousMeasurement,
    DiscreteMeasurement,
    Measurement,
)

T = TypeVar("T", bound=Measurement)


def get_subsequence(sequence: list[T], start: int, stop: int) -> tuple[list[T], int, int]:
    """Gets the sub-sequence of measurements or items with timestamps within the given
    range.

    T: bounded with Measurement.

    Args:
        sequence: Sequence of items to get a sub-sequence from.

        start: Left timestamp limit (inclusive).

        stop: Right timestamp limit (exclusive).

    Returns:
        A subsequence within the given range, start index, stop index.
    """
    if not sequence or start >= stop:
        raise ValueError("Empty sequence or invalid limits.")

    timestamps: list[int] = [item.timestamp for item in sequence]
    start_idx = bisect_left(timestamps, start)
    stop_idx = bisect_left(timestamps, stop)

    return sequence[start_idx:stop_idx], start_idx, stop_idx


def fill_connections(
    item: ClustersWithConnections, measurement: ContinuousMeasurement
) -> list[DiscreteMeasurement]:
    """Fills connections with continuous measurements.

    Args:
        item: clusters and their connections.

        measurement: continuous measurement to be used for connections.

    Returns:
        unused discrete measurements.
    """
    used_elements: set[DiscreteMeasurement] = set()
    for connection in item.connections:
        start = connection.cluster1.timestamp
        stop = connection.cluster2.timestamp
        elements, _, stop = get_subsequence(measurement.elements, start, stop)
        new_measurement = ContinuousMeasurement(elements)
        connection.cluster2.add(new_measurement)
        used_elements.update(elements)

    leftovers = [el for el in measurement.elements if el not in used_elements]
    return leftovers


def create_1_cluster_with_leftovers(
    cluster: Cluster, measurement: ContinuousMeasurement
) -> ClustersWithLeftovers:
    """Creates a structure with 1 cluster and leftovers using the elements of the
    measurement.

    Args:
        cluster: cluster to add a measurement in.

        measurement: measurement to use elements of.

    Returns:
        structure with clusters and leftovers.
    """

    start = measurement.time_range.start
    stop = cluster.timestamp
    elements, _, stop_idx = get_subsequence(measurement.elements, start, stop)
    leftovers = measurement.elements[stop_idx:]
    new_measurement = ContinuousMeasurement(elements)
    cluster.add(new_measurement)
    return ClustersWithLeftovers([cluster], leftovers)


def add_left_tail(
    cluster: Cluster, measurement: ContinuousMeasurement
) -> list[DiscreteMeasurement]:
    """Creates a continuous measurement using all discrete elements before the cluster`s
    timestamp.

    Args:
        cluster: cluster to add a continuous measurement in.

        measurement: continuous measurement with discrete elements.

    Returns:
        used elements.
    """
    start = measurement.elements[0].timestamp
    stop = cluster.timestamp
    elements, _, _ = get_subsequence(measurement.elements, start, stop)
    cluster.add(ContinuousMeasurement(elements))
    return elements


def remove_elements(
    list_to_update: list[DiscreteMeasurement], elements_to_remove: list[DiscreteMeasurement]
) -> list[DiscreteMeasurement]:
    """Removes elements from the list.

    Args:
        list_to_update: list to be updated.

        elements_to_remove: elements to be removed from the list.
    """
    remove_set = set(elements_to_remove)
    return [el for el in list_to_update if el not in remove_set]


def create_clusters_with_leftovers(
    clusters: list[Cluster],
    measurement: ContinuousMeasurement,
    elements: list[DiscreteMeasurement],
) -> ClustersWithLeftovers:
    """Creates a structure with clusters and unused measurements.

    Args:
        clusters: clusters with discrete measurements.

        measurement: continuous measurement.

        elements: discrete elements to be filtered.

    Returns:
        clusters with unused measurements.
    """
    used_elements = add_left_tail(clusters[0], measurement)
    leftovers = remove_elements(elements, used_elements)
    variant = ClustersWithLeftovers(clusters, leftovers)
    return variant


def create_clusters_with_leftovers_combinations(
    clusters_combinations: list[list[Cluster]], measurement: ContinuousMeasurement
) -> list[ClustersWithLeftovers]:
    """Creates combinations of clusters with unused elements of a continuous
    measurement.

    Args:
        clusters_combinations: combinations of clusters.

        measurement: continuous measurement to use elements of.

    Returns:
        combinations of clusters and corresponding unused elements.
    """

    variants: list[ClustersWithLeftovers] = []

    for clusters in clusters_combinations:

        if len(clusters) == 1:
            clusters_copy = deepcopy(clusters)
            v = create_clusters_with_leftovers(clusters_copy, measurement, measurement.elements)
            variants.append(v)
            continue

        combinations = ConnectionsFactory.create_combinations(clusters)
        # TODO: filter irrealizable combinations here due to continuous sensors limitations.

        for connections in combinations:
            item = deepcopy(ClustersWithConnections(clusters, connections))
            leftovers = fill_connections(item, measurement)
            v = create_clusters_with_leftovers(item.clusters, measurement, leftovers)
            variants.append(v)

    return variants
