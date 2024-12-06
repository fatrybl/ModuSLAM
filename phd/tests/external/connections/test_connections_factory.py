from phd.bridge.auxiliary_dataclasses import Connection
from phd.external.connections.connections_factory import Factory
from phd.measurements.auxiliary_classes import PseudoMeasurement
from phd.measurements.cluster import Cluster


def test_create_combinations_single_cluster():
    cluster = Cluster()
    cluster.add(PseudoMeasurement(1, "a"))
    clusters = [cluster]
    result = Factory.create_combinations(clusters)
    assert result == []


def test_create_combinations_encode_decode():
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    cluster1.add(PseudoMeasurement(1, "a"))
    cluster2.add(PseudoMeasurement(2, "b"))
    cluster3.add(PseudoMeasurement(3, "c"))
    clusters = [cluster1, cluster2, cluster3]

    result = Factory.create_combinations(clusters)

    assert len(result) > 0

    for combination in result:
        assert len(combination) > 0
        for connection in combination:
            assert isinstance(connection, Connection)
            assert connection.cluster1 in clusters
            assert connection.cluster2 in clusters
            assert connection.cluster1 != connection.cluster2


def test_create_combinations_multiple_clusters_multiple_measurements():
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    cluster1.add(PseudoMeasurement(1, "a"))
    cluster1.add(PseudoMeasurement(2, "b"))
    cluster2.add(PseudoMeasurement(3, "c"))
    cluster2.add(PseudoMeasurement(4, "d"))
    cluster3.add(PseudoMeasurement(5, "e"))
    cluster3.add(PseudoMeasurement(6, "f"))
    clusters = [cluster1, cluster2, cluster3]

    result = Factory.create_combinations(clusters)

    assert len(result) > 0

    # Check if all possible cluster pairs are present in the combinations
    all_pairs = set()
    for combination in result:
        for connection in combination:
            pair = frozenset([connection.cluster1, connection.cluster2])
            all_pairs.add(pair)

    expected_pairs = {
        frozenset([clusters[0], clusters[1]]),
        frozenset([clusters[1], clusters[2]]),
        frozenset([clusters[0], clusters[2]]),
    }
    assert all_pairs == expected_pairs


def test_create_combinations_with_duplicate_measurements():
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    cluster1.add(PseudoMeasurement(1, "a"))
    cluster1.add(PseudoMeasurement(2, "b"))
    cluster2.add(PseudoMeasurement(1, "a"))  # Duplicate measurement
    cluster2.add(PseudoMeasurement(3, "c"))
    cluster3.add(PseudoMeasurement(4, "d"))
    clusters = [cluster1, cluster2, cluster3]

    result = Factory.create_combinations(clusters)

    expected_pairs = {
        frozenset([clusters[0], clusters[1]]),
        frozenset([clusters[1], clusters[2]]),
        frozenset([clusters[0], clusters[2]]),
    }

    assert len(result) > 0

    # Check if all possible cluster pairs are present in the combinations
    all_pairs = set()
    for combination in result:
        for connection in combination:
            pair = frozenset([connection.cluster1, connection.cluster2])
            all_pairs.add(pair)

    assert all_pairs == expected_pairs

    # Check if duplicate measurements don't affect the result
    for combination in result:
        for connection in combination:
            assert connection.cluster1 != connection.cluster2
