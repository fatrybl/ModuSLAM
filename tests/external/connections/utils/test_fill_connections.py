from moduslam.bridge.auxiliary_dataclasses import ClustersWithConnections, Connection
from moduslam.external.connections.utils import fill_multiple_connections
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import (
    FakeMeasurement,
    PseudoMeasurement,
)
from moduslam.measurement_storage.measurements.imu import ContinuousImu, Imu, ImuData
from moduslam.utils.auxiliary_objects import zero_vector3


def test_1_connection_in_between():
    t1, t2, t3, t4, t5 = 0, 1, 2, 3, 4
    core1, core2 = PseudoMeasurement(t1), PseudoMeasurement(t5)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(core1)
    cluster2.add(core2)
    con1 = Connection(cluster1, cluster2)
    clusters = [cluster1, cluster2]
    connections = [con1]
    item = ClustersWithConnections(clusters, connections)
    measurements = [Imu(t, ImuData(zero_vector3, zero_vector3)) for t in [t2, t3, t4]]

    filled_clusters, leftovers, num_unused = fill_multiple_connections(item, measurements)

    assert len(filled_clusters) == 2
    filled1, filled2 = filled_clusters
    continuous = filled2.measurements[1]

    assert num_unused == 0
    assert filled1 is cluster1
    assert filled2 is cluster2
    assert leftovers == []
    assert len(filled1.measurements) == 1
    assert filled1.measurements[0] is core1
    assert len(filled2.measurements) == 2
    assert filled2.measurements[0] is core2
    assert isinstance(continuous, ContinuousImu)
    assert filled1.timestamp == t1
    assert filled2.timestamp == t5
    assert filled1.time_range.start == filled1.time_range.stop == t1
    assert filled2.time_range.start == filled2.time_range.stop == t5
    assert continuous.timestamp == t5
    assert continuous.time_range.start == cluster1.timestamp
    assert continuous.time_range.stop == cluster2.timestamp
    assert continuous.items == measurements


def test_1_connection_with_left_tail_1():
    t1, t2, t3, t4, t5 = 0, 1, 2, 3, 4
    fake = FakeMeasurement(t1)
    core1, core2 = PseudoMeasurement(t2), PseudoMeasurement(t5)
    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()
    cluster1.add(fake)
    cluster2.add(core1)
    cluster3.add(core2)
    clusters = [cluster1, cluster2, cluster3]
    connections = [Connection(cluster1, cluster3)]  # connects tail and the last cluster.
    item = ClustersWithConnections(clusters, connections)
    measurements = [Imu(t, ImuData(zero_vector3, zero_vector3)) for t in [t1, t3, t4]]

    filled_clusters, leftovers, num_unused = fill_multiple_connections(item, measurements)

    assert num_unused == 0
    assert len(filled_clusters) == 2

    filled1, filled2 = filled_clusters
    continuous = filled2.measurements[1]

    assert filled1 is cluster2
    assert filled2 is cluster3

    assert leftovers == []
    assert filled1.measurements[0] is core1
    assert filled2.measurements[0] is core2
    assert len(filled1.measurements) == 1
    assert len(filled2.measurements) == 2
    assert isinstance(continuous, ContinuousImu)
    assert filled1.timestamp == t2
    assert filled2.timestamp == t5
    assert filled1.time_range.start == filled1.time_range.stop == t2
    assert filled2.time_range.start == filled2.time_range.stop == t5
    assert len(continuous.items) == 3


def test_with_left_tail_2():
    t1, t2, t3, t4, t5 = 0, 1, 2, 3, 4
    fake = FakeMeasurement(t1)
    core1, core2 = PseudoMeasurement(t2), PseudoMeasurement(t5)
    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()
    cluster1.add(fake)
    cluster2.add(core1)
    cluster3.add(core2)
    con1 = Connection(cluster1, cluster2)
    con2 = Connection(cluster2, cluster3)
    clusters = [cluster1, cluster2, cluster3]
    connections = [con1, con2]  # connects tail with 1-st and 1-st with 2-nd cluster.
    item = ClustersWithConnections(clusters, connections)
    measurements = [Imu(t, ImuData(zero_vector3, zero_vector3)) for t in [t1, t3, t4]]

    filled_clusters, leftovers, num_unused = fill_multiple_connections(item, measurements)

    assert num_unused == 0
    assert len(filled_clusters) == 2

    filled1, filled2 = filled_clusters
    continuous1 = filled1.measurements[1]
    continuous2 = filled2.measurements[1]

    assert filled1 is cluster2
    assert filled2 is cluster3

    assert leftovers == []
    assert filled1.measurements[0] is core1
    assert filled2.measurements[0] is core2
    assert len(filled1.measurements) == 2
    assert len(filled2.measurements) == 2
    assert isinstance(continuous1, ContinuousImu)
    assert isinstance(continuous2, ContinuousImu)
    assert filled1.timestamp == t2
    assert filled2.timestamp == t5
    assert filled1.time_range.start == filled1.time_range.stop == t2
    assert filled2.time_range.start == filled2.time_range.stop == t5
    assert continuous1.timestamp == t2
    assert continuous1.time_range.start == t1
    assert continuous1.time_range.stop == t2
    assert len(continuous1.items) == 1
    assert len(continuous2.items) == 2


def test_with_left_tail_and_leftover():
    t1, t2, t3, t4, t5, t6 = 0, 1, 2, 3, 4, 5
    fake = FakeMeasurement(t1)
    core1, core2 = PseudoMeasurement(t2), PseudoMeasurement(t5)
    cluster1, cluster2, cluster3 = MeasurementCluster(), MeasurementCluster(), MeasurementCluster()
    cluster1.add(fake)
    cluster2.add(core1)
    cluster3.add(core2)
    con1 = Connection(cluster1, cluster2)
    con2 = Connection(cluster2, cluster3)
    clusters = [cluster1, cluster2, cluster3]
    connections = [con1, con2]
    item = ClustersWithConnections(clusters, connections)
    measurements = [Imu(t, ImuData(zero_vector3, zero_vector3)) for t in [t1, t3, t4, t6]]

    filled_clusters, leftovers, num_unused = fill_multiple_connections(item, measurements)

    assert num_unused == 0
    assert len(filled_clusters) == 2

    filled1, filled2 = filled_clusters
    continuous1 = filled1.measurements[1]
    continuous2 = filled2.measurements[1]

    assert filled1 is cluster2
    assert filled2 is cluster3

    assert len(leftovers) == 1
    assert leftovers[0].timestamp == t6

    assert filled1.measurements[0] is core1
    assert filled2.measurements[0] is core2
    assert len(filled1.measurements) == 2
    assert len(filled2.measurements) == 2
    assert isinstance(continuous1, ContinuousImu)
    assert isinstance(continuous2, ContinuousImu)
    assert filled1.timestamp == t2
    assert filled2.timestamp == t5
    assert filled1.time_range.start == filled1.time_range.stop == t2
    assert filled2.time_range.start == filled2.time_range.stop == t5
    assert continuous1.timestamp == t2
    assert continuous1.time_range.start == t1
    assert continuous1.time_range.stop == t2
    assert len(continuous1.items) == 1
    assert len(continuous2.items) == 2


def test_with_num_unused_and_leftovers():
    t1, t2, t3, t4, t5, t6 = 0, 1, 2, 3, 4, 5
    core1, core2 = PseudoMeasurement(t2), PseudoMeasurement(t5)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(core1)
    cluster2.add(core2)
    clusters = [cluster1, cluster2]
    connections = [Connection(cluster1, cluster2)]
    item = ClustersWithConnections(clusters, connections)
    measurements = [Imu(t, ImuData(zero_vector3, zero_vector3)) for t in [t1, t3, t4, t6]]

    filled_clusters, leftovers, num_unused = fill_multiple_connections(item, measurements)

    assert num_unused == 1
    assert len(leftovers) == 1
    assert len(filled_clusters) == 2

    filled1, filled2 = filled_clusters
    continuous = filled2.measurements[1]

    assert filled1 is cluster1
    assert filled2 is cluster2

    assert leftovers[0].timestamp == t6

    assert filled1.measurements[0] is core1
    assert filled2.measurements[0] is core2
    assert len(filled1.measurements) == 1
    assert len(filled2.measurements) == 2
    assert isinstance(continuous, ContinuousImu)
    assert filled1.timestamp == t2
    assert filled2.timestamp == t5
    assert filled1.time_range.start == filled1.time_range.stop == t2
    assert filled2.time_range.start == filled2.time_range.stop == t5
    assert continuous.time_range.start == t2
    assert continuous.time_range.stop == t5
    assert len(continuous.items) == 2
