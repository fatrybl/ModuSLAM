from moduslam.bridge.auxiliary_dataclasses import (
    ClustersWithConnections,
    ClustersWithLeftovers,
)
from moduslam.external.connections.connections_factory import Factory
from moduslam.external.utils import copy_cluster, create_copy, get_subsequence
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import FakeMeasurement
from moduslam.measurement_storage.measurements.imu import ContinuousImu, Imu


def fill_one_connection(
    cluster: MeasurementCluster, measurements: list[Imu], left_limit_t: int | None
) -> tuple[int, list[Imu]]:
    """Adds a continuous IMU measurement to the cluster, fills leftovers and computes
    the number of unused measurements.

    Args:
        cluster: a cluster to be copied.

        measurements: discrete IMU measurements to fill in the connections.

        left_limit_t: the left time limit for the 1-st IMU measurement.

    Returns:
        number of unused measurements, leftovers for future processing.
    """
    t = cluster.timestamp
    first_imu_t = measurements[0].timestamp
    last_imu_t = measurements[-1].timestamp
    first_core_t = cluster.time_range.start

    num_unused: int = 0
    leftovers: list[Imu] = []

    if len(cluster.core_measurements) == 1 and first_imu_t >= t:
        return 0, measurements

    if last_imu_t >= t:
        leftovers, _, _ = get_subsequence(measurements, t, last_imu_t, inclusive_stop=True)

    if first_imu_t < first_core_t:
        start = min(first_imu_t, left_limit_t) if left_limit_t is not None else first_imu_t
        subsequence, _, _ = get_subsequence(measurements, start, t, inclusive_stop=False)
        measurement = ContinuousImu(subsequence, start, t)
        cluster.add(measurement)

    else:
        _, _, right_idx = get_subsequence(measurements, first_core_t, t, inclusive_stop=False)
        num_unused = right_idx

    return num_unused, leftovers


def fill_multiple_connections(
    item: ClustersWithConnections, measurements: list[Imu]
) -> tuple[list[MeasurementCluster], list[Imu], int]:
    """Replaces virtual connections with continuous IMU measurements.

    Args:
        item: clusters and connections.

        measurements: discrete IMU measurements to create continuous IMU measurements.

    Returns:
        1: filled clusters.
        2: unused discrete IMU measurements for future processing.
        3: number of unused IMU measurements.
    """
    first_imu_t = measurements[0].timestamp
    first_cluster_t = item.clusters[0].timestamp
    last_cluster = item.clusters[-1]
    leftovers: list[Imu] = []
    num_unused: int = 0

    for connection in item.connections:
        cls1, cls2 = connection.cluster1, connection.cluster2
        start, stop = cls1.timestamp, cls2.timestamp

        subsequence, _, _ = get_subsequence(measurements, start, stop, False)
        if not subsequence:
            continue

        m = ContinuousImu(subsequence, start, stop)
        connection.cluster2.add(m)

        if cls1.fake_measurements:
            item.clusters.remove(cls1)

        current_leftovers = get_leftovers(cls2, last_cluster, measurements)
        if current_leftovers:
            leftovers = current_leftovers

    if first_imu_t < first_cluster_t:
        _, _, idx = get_subsequence(measurements, first_imu_t, first_cluster_t, False)
        num_unused = idx

    return item.clusters, leftovers, num_unused


def get_leftovers(
    current: MeasurementCluster, last: MeasurementCluster, measurements: list[Imu]
) -> list[Imu]:
    """Gets unused IMU measurements. Only for the last cluster.

    Args:
        current: a current cluster with core measurements.

        last: the last cluster with core measurements.

        measurements: IMU measurements to compute leftovers.

    Returns:
        unused IMU measurements or None.
    """
    leftovers: list[Imu] = []
    if current is last:
        start = last.timestamp
        stop = measurements[-1].timestamp

        if stop >= start:
            leftovers, _, _ = get_subsequence(measurements, start, stop, inclusive_stop=True)

    return leftovers


def create_and_fill_connections(
    clusters_combinations: list[list[MeasurementCluster]],
    measurements: list[Imu],
    first_core_t: int,
    left_limit_t: int | None,
) -> list[ClustersWithLeftovers]:
    """Creates combinations of clusters and unused measurements.

    Args:
        clusters_combinations: combinations of clusters.

        measurements: IMU measurements to fill in the connections.

        left_limit_t: the timestamp of the latest vertex in vertex cluster.

        first_core_t: the timestamp of the 1-st core measurement.

    Returns:
        combinations of clusters with corresponding unused elements.
    """
    variants: list[ClustersWithLeftovers] = []
    first_imu_t = measurements[0].timestamp

    for clusters in clusters_combinations:

        if len(clusters) == 1:
            cluster = copy_cluster(clusters[0])
            num_unused, leftovers = fill_one_connection(cluster, measurements, left_limit_t)
            variants.append(ClustersWithLeftovers([cluster], leftovers, num_unused))

        else:
            if first_imu_t < first_core_t:
                add_fake_cluster(clusters, first_imu_t, left_limit_t)

            combinations = Factory.create_combinations(clusters)

            for connections in combinations:
                clusters_copy, connections_copy = create_copy(clusters, connections)
                item = ClustersWithConnections(clusters_copy, connections_copy)
                new_clusters, leftovers, unused = fill_multiple_connections(item, measurements)
                v = ClustersWithLeftovers(new_clusters, leftovers, unused)
                variants.append(v)

    return variants


def add_fake_cluster(
    clusters: list[MeasurementCluster], first_imu_t: int, left_limit_t: int | None
):
    """Adds fake cluster with fake measurement if the 1-st IMU measurement is earlier
    than the 1-st Core measurement in the Cluster.

    Args:
        clusters: list of measurement clusters.

        first_imu_t: timestamp of the 1-st IMU measurement.

        left_limit_t: a left time limit.
    """
    if left_limit_t is None:
        t = first_imu_t
    else:
        t = min(first_imu_t, left_limit_t)

    fake_m = FakeMeasurement(t)
    fake_cluster = MeasurementCluster()
    fake_cluster.add(fake_m)
    clusters.insert(0, fake_cluster)
