from phd.external.objects.auxiliary_objects import Connection
from phd.external.objects.measurements import CoreMeasurement
from phd.external.objects.measurements_cluster import Cluster
from phd.external.utils import create_copy


def test_create_copy_with_empty_inputs():
    clusters: list[Cluster] = []
    connections: list[Connection] = []

    copied_clusters, copied_connections = create_copy(clusters, connections)

    assert copied_clusters == []
    assert copied_connections == []


def test_create_copy_single_cluster_no_connections():
    cluster = Cluster()
    measurement1 = CoreMeasurement(timestamp=1, value="a")
    measurement2 = CoreMeasurement(timestamp=2, value="b")
    cluster.add(measurement1)
    cluster.add(measurement2)

    clusters = [cluster]
    connections: list[Connection] = []

    copied_clusters, copied_connections = create_copy(clusters, connections)

    assert len(copied_clusters) == 1
    assert copied_clusters[0] != cluster
    assert copied_clusters[0].measurements == cluster.measurements
    assert copied_connections == []


def test_create_copy_single_connection_between_clusters():
    cluster1, cluster2 = Cluster(), Cluster()
    measurement1 = CoreMeasurement(timestamp=1, value="a")
    measurement2 = CoreMeasurement(timestamp=2, value="b")

    cluster1.add(measurement1)
    cluster2.add(measurement2)

    connection = Connection(cluster1, cluster2)

    clusters = [cluster1, cluster2]
    connections = [connection]

    copied_clusters, copied_connections = create_copy(clusters, connections)

    assert len(copied_clusters) == 2
    assert copied_clusters[0] != cluster1
    assert copied_clusters[1] != cluster2
    assert copied_clusters[0].measurements == cluster1.measurements
    assert copied_clusters[1].measurements == cluster2.measurements

    assert len(copied_connections) == 1
    copied_connection = copied_connections[0]
    assert copied_connection.cluster1 == copied_clusters[0]
    assert copied_connection.cluster2 == copied_clusters[1]


def test_create_copy_multiple_connections_between_multiple_clusters():
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    measurement1 = CoreMeasurement(timestamp=1, value="a")
    measurement2 = CoreMeasurement(timestamp=2, value="b")
    measurement3 = CoreMeasurement(timestamp=3, value="c")

    cluster1.add(measurement1)
    cluster2.add(measurement2)
    cluster3.add(measurement3)

    connection1 = Connection(cluster1, cluster2)
    connection2 = Connection(cluster2, cluster3)
    connection3 = Connection(cluster1, cluster3)

    clusters = [cluster1, cluster2, cluster3]
    connections = [connection1, connection2, connection3]

    copied_clusters, copied_connections = create_copy(clusters, connections)

    assert len(copied_clusters) == 3
    assert copied_clusters[0] != cluster1
    assert copied_clusters[1] != cluster2
    assert copied_clusters[2] != cluster3
    assert copied_clusters[0].measurements == cluster1.measurements
    assert copied_clusters[1].measurements == cluster2.measurements
    assert copied_clusters[2].measurements == cluster3.measurements

    assert len(copied_connections) == 3
    assert copied_connections[0].cluster1 == copied_clusters[0]
    assert copied_connections[0].cluster2 == copied_clusters[1]
    assert copied_connections[1].cluster1 == copied_clusters[1]
    assert copied_connections[1].cluster2 == copied_clusters[2]
    assert copied_connections[2].cluster1 == copied_clusters[0]
    assert copied_connections[2].cluster2 == copied_clusters[2]


def test_create_copy_maintains_order():
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    measurement1 = CoreMeasurement(timestamp=1, value="a")
    measurement2 = CoreMeasurement(timestamp=2, value="b")
    measurement3 = CoreMeasurement(timestamp=3, value="c")

    cluster1.add(measurement1)
    cluster2.add(measurement2)
    cluster3.add(measurement3)

    connection1 = Connection(cluster1, cluster2)
    connection2 = Connection(cluster2, cluster3)
    connection3 = Connection(cluster1, cluster3)

    clusters = [cluster1, cluster2, cluster3]
    connections = [connection1, connection2, connection3]

    copied_clusters, copied_connections = create_copy(clusters, connections)

    assert copied_clusters[0].measurements == cluster1.measurements
    assert copied_clusters[1].measurements == cluster2.measurements
    assert copied_clusters[2].measurements == cluster3.measurements

    assert copied_connections[0].cluster1 == copied_clusters[0]
    assert copied_connections[0].cluster2 == copied_clusters[1]
    assert copied_connections[1].cluster1 == copied_clusters[1]
    assert copied_connections[1].cluster2 == copied_clusters[2]
    assert copied_connections[2].cluster1 == copied_clusters[0]
    assert copied_connections[2].cluster2 == copied_clusters[2]


def test_create_copy_modifying_copies_does_not_affect_originals():
    cluster1, cluster2 = Cluster(), Cluster()
    measurement1 = CoreMeasurement(timestamp=1, value="a")
    measurement2 = CoreMeasurement(timestamp=2, value="b")

    cluster1.add(measurement1)
    cluster2.add(measurement2)

    connection = Connection(cluster1, cluster2)

    clusters = [cluster1, cluster2]
    connections = [connection]

    copied_clusters, copied_connections = create_copy(clusters, connections)

    copied_clusters[0].add(CoreMeasurement(timestamp=3, value="c"))
    copied_connections[0].cluster1 = copied_clusters[1]

    assert len(cluster1.measurements) == 1
    assert len(cluster2.measurements) == 1
    assert cluster1.measurements[0].value == "a"
    assert cluster2.measurements[0].value == "b"

    assert connection.cluster1 == cluster1
    assert connection.cluster2 == cluster2
