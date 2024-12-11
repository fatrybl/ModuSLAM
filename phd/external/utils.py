from bisect import bisect_left
from collections import defaultdict
from collections.abc import Iterable
from typing import TypeVar

from phd.bridge.auxiliary_dataclasses import ClustersWithLeftovers, Connection
from phd.measurement_storage.cluster import Cluster
from phd.measurement_storage.measurementgroup import MeasurementGroup
from phd.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.continuous import ContinuousMeasurement

T = TypeVar("T", bound=Measurement)


def get_subsequence(sequence: list[T], start: int, stop: int) -> tuple[list[T], int, int]:
    """Gets the sub-sequence of items within the given range for the sorted sequence.

    Args:
        sequence: a sorted with timestamps sequence of items to get a sub-sequence of.

        start: index of left timestamp limit (inclusive).

        stop: index of right timestamp limit (exclusive).

    Returns:
        a subsequence of the given range, start index, stop index.
    """
    if not sequence or start > stop:
        raise ValueError("Empty sequence or invalid limits.")

    timestamps: list[int] = [item.timestamp for item in sequence]
    start_idx = bisect_left(timestamps, start)
    stop_idx = bisect_left(timestamps, stop)

    return sequence[start_idx:stop_idx], start_idx, stop_idx


def copy_cluster(cluster: Cluster) -> Cluster:
    """Creates a cluster with the same measurements as in the given cluster.

    Args:
        cluster: cluster to copy measurements from.

    Returns:
        new cluster with the same measurements.
    """
    new_cluster = Cluster()
    for m in cluster.measurements:
        new_cluster.add(m)
    return new_cluster


def create_copy(
    clusters: list[Cluster], connections: list[Connection]
) -> tuple[list[Cluster], list[Connection]]:
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
            current_measurements: list[Measurement] = []

            for m in cluster.measurements:
                if isinstance(m, ContinuousMeasurement):
                    current_measurements += m.items
                else:
                    current_measurements.append(m)

            measurements_list.append(tuple(current_measurements))

        measurements = tuple(measurements_list)
        key = (measurements, leftovers)

        if key not in seen:
            seen.add(key)
            unique_clusters_with_leftovers.append(clusters_with_leftovers)

    return unique_clusters_with_leftovers


def group_by_timestamp(measurements: Iterable[Measurement]) -> list[MeasurementGroup]:
    """Groups measurements by timestamp.

    Args:
        measurements: measurements to group by timestamp.

    Returns:
         measurements` groups.
    """
    groups: dict[int, MeasurementGroup] = defaultdict(MeasurementGroup)

    for m in measurements:
        groups[m.timestamp].measurements.add(m)

    return list(groups.values())


def remove_loops(combinations: list[list[Cluster]]) -> list[list[Cluster]]:
    """Removes combinations which have clusters with loops.
    Loop - a cluster which has multiple SplitPoseOdometry measurements with the same parent.

    Args:
        combinations: combinations of clusters.

    Returns:
        combinations without loops.
    """

    new_combinations = []

    for combination in combinations:
        clusters = []
        for cluster in combination:
            split_odometries = [m for m in cluster.measurements if isinstance(m, SplitPoseOdometry)]
            num_unique_parents = len(set([m.parent for m in split_odometries]))
            num_all_parents = len([m.parent for m in split_odometries])
            if num_unique_parents == num_all_parents:
                clusters.append(cluster)
            else:
                break

        if len(clusters) == len(combination):
            new_combinations.append(clusters)

    return new_combinations
