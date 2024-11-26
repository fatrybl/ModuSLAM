class MockCluster:
    def __init__(self, timestamp, time_range_start, time_range_stop):
        self.timestamp = timestamp
        self.time_range = MockTimeRange(time_range_start, time_range_stop)


class MockTimeRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop


class MockVertexStorage:
    def __init__(self, clusters):
        self.clusters = clusters


def get_closest_cluster(storage, timestamp, threshold):
    """Gets the closest cluster for the given timestamp and threshold.

    Args:
        storage: a storage with clusters.
        timestamp: a timestamp.
        threshold: a threshold in seconds for the distance between timestamps.

    Returns:
        The closest cluster if one exists within the threshold, otherwise None.
    """
    for cluster in reversed(storage.clusters):

        if abs(timestamp - cluster.time_range.stop) <= threshold:
            return cluster

        if abs(cluster.time_range.start - timestamp) <= threshold:
            return cluster

        if cluster.time_range.start <= timestamp <= cluster.time_range.stop:
            return cluster

        if abs(cluster.time_range.stop + threshold) < timestamp:
            break

    return None


def test_no_clusters():
    storage = MockVertexStorage([])
    assert get_closest_cluster(storage, 100, 10) is None


def test_single_valid_cluster():
    cluster = MockCluster(100, 90, 110)
    storage = MockVertexStorage([cluster])
    result = get_closest_cluster(storage, 105, 10)
    assert result == cluster


def test_multiple_non_overlapping_clusters():
    cluster1 = MockCluster(90, 80, 100)
    cluster2 = MockCluster(110, 100, 120)
    storage = MockVertexStorage([cluster1, cluster2])
    result = get_closest_cluster(storage, 115, 10)
    assert result == cluster2  # Closest to 115


def test_no_match_outside_all_clusters():
    cluster1 = MockCluster(50, 40, 60)
    cluster2 = MockCluster(100, 90, 110)
    storage = MockVertexStorage([cluster1, cluster2])
    assert get_closest_cluster(storage, 200, 10) is None


def test_match_at_boundary():
    cluster = MockCluster(100, 90, 110)
    storage = MockVertexStorage([cluster])
    result = get_closest_cluster(storage, 90, 10)
    assert result == cluster


def test_early_termination():
    cluster1 = MockCluster(10, 0, 20)
    cluster2 = MockCluster(50, 40, 60)
    cluster3 = MockCluster(100, 90, 110)
    storage = MockVertexStorage([cluster1, cluster2, cluster3])
    result = get_closest_cluster(storage, 55, 10)
    assert result == cluster2
