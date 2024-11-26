import pytest

from phd.bridge.edge_factories.gps_position import Factory
from phd.measurements.processed_measurements import Gps
from phd.moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from phd.moduslam.data_manager.batch_factory.readers.locations import Location
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.setup_manager.sensors_factory.sensors import Gps as GpsSensor
from phd.moduslam.setup_manager.sensors_factory.sensors_configs import SensorConfig
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, zero_vector3


@pytest.fixture
def gps() -> Gps:
    cfg = SensorConfig(name="gps")
    measurement = RawMeasurement(GpsSensor(cfg), zero_vector3)
    element = Element(0, measurement, Location())
    return Gps(element, zero_vector3, identity3x3)


@pytest.fixture
def gps_at_1() -> Gps:
    cfg = SensorConfig(name="gps")
    measurement = RawMeasurement(GpsSensor(cfg), zero_vector3)
    element = Element(1, measurement, Location())
    return Gps(element, zero_vector3, identity3x3)


def test_create_empty_graph(empty_graph: Graph, gps: Gps):
    t = 0
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(empty_graph, clusters, gps)
    edge_vertex = new_element.edge.vertex
    new_pose, timestamp = new_element.new_vertices[cluster][0]

    assert len(new_element.new_vertices) == 1
    assert new_pose.index == 0
    assert timestamp == t
    assert edge_vertex is new_pose


def test_create_graph_with_1_existing_vertex(graph1: Graph, gps: Gps):
    clusters = {VertexCluster(): TimeRange(0, 0)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)

    new_element = Factory.create(graph1, clusters, gps)
    vertex = new_element.edge.vertex

    assert not new_element.new_vertices
    assert vertex is existing_vertex


def test_create_graph_with_1_existing_1_new_vertex(graph1: Graph, gps_at_1: Gps):
    t = 1
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)

    new_element = Factory.create(graph1, clusters, gps_at_1)
    vertex, timestamp = new_element.new_vertices[cluster][0]

    assert len(new_element.new_vertices) == 1
    assert vertex is not existing_vertex
    assert vertex.index == 1
    assert timestamp == t
