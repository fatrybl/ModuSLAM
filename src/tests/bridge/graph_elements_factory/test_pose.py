"""Tests create_graph_element() method with pose measurements."""

from src.bridge.candidates_factory import create_graph_elements
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4


def test_no_data(empty_graph: Graph):
    elements = create_graph_elements(empty_graph, [])
    assert elements == []


def test_2_measurements_empty_graph(empty_graph: Graph):
    m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(1, i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)

    elements = create_graph_elements(empty_graph, [cluster1, cluster2])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices != elem2.new_vertices
    assert len(elem1.new_vertices) == 1
    assert len(elem2.new_vertices) == 1

    assert e1 is not e2
    assert e1.index == 0
    assert e2.index == 1

    v1, v2 = elem1.new_vertices[0], elem2.new_vertices[0]
    assert v1 is not v2
    assert v1.timestamp == 0
    assert v2.timestamp == 1
    assert v1.instance.index == 0
    assert v2.instance.index == 1
    assert e1.vertex is v1.instance
    assert e2.vertex is v2.instance
    assert v1.instance.value == v2.instance.value == i4x4


def test_2_measurements_equal_time_empty_graph(empty_graph: Graph):
    m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(m1)
    cluster.add(m2)

    elements = create_graph_elements(empty_graph, [cluster])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices != elem2.new_vertices
    assert len(elem1.new_vertices) == 1
    assert len(elem2.new_vertices) == 0
    assert len(e1.vertices) == 1
    assert len(e2.vertices) == 1
    assert e1 is not e2
    assert e1.index == 0
    assert e2.index == 1

    v1 = elem1.edge.vertices[0]
    v2 = elem2.edge.vertices[0]

    assert v1 is v2


def test_2_measurements_equal_time_graph1(graph1: Graph):
    m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(m1)
    cluster.add(m2)
    existing_v = graph1.vertex_storage.get_last_vertex(Pose)

    elements = create_graph_elements(graph1, [cluster])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices == elem2.new_vertices == []
    assert len(e1.vertices) == 1
    assert len(e2.vertices) == 1
    assert e1 is not e2
    assert e1.index == 1
    assert e2.index == 2

    v1 = elem1.edge.vertices[0]
    v2 = elem2.edge.vertices[0]

    assert v1 is v2 is existing_v


def test_2_measurements_different_time_graph1(graph1: Graph):
    m1 = PoseMeasurement(1, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(2, i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)
    existing_v = graph1.vertex_storage.get_last_vertex(Pose)

    elements = create_graph_elements(graph1, [cluster1, cluster2])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices != elem2.new_vertices
    assert len(elem1.new_vertices) == 1
    assert len(elem2.new_vertices) == 1

    assert e1 is not e2
    assert e1.index == 1
    assert e2.index == 2

    v1, v2 = elem1.new_vertices[0], elem2.new_vertices[0]
    assert v1 is not v2
    assert v1 is not existing_v and v2 is not existing_v
    assert v1.timestamp == 1
    assert v2.timestamp == 2
    assert v1.instance.index == 1
    assert v2.instance.index == 2
    assert e1.vertex is v1.instance
    assert e2.vertex is v2.instance


def test_2_measurements_no_new_vertices_graph2(graph2: Graph):
    m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(1, i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    elements = create_graph_elements(graph2, [cluster1, cluster2])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices == elem2.new_vertices == []

    assert e1 is not e2
    assert e1.index == 2
    assert e2.index == 3

    v1 = elem1.edge.vertices[0]
    v2 = elem2.edge.vertices[0]

    assert v1 is not v2
    assert v1 is existing_v1
    assert v2 is existing_v2


def test_2_measurements_1_new_vertex_graph2(graph2: Graph):
    m1 = PoseMeasurement(1, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(2, i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    elements = create_graph_elements(graph2, [cluster1, cluster2])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert len(elem1.new_vertices) == 0
    assert len(elem2.new_vertices) == 1

    assert e1 is not e2
    assert e1.index == 2
    assert e2.index == 3

    v1 = elem1.edge.vertices[0]
    v2 = elem2.edge.vertices[0]

    assert v1 is not v2
    assert v1 is existing_v2
    assert v2 is not existing_v1 and v2 is not existing_v2


def test_2_measurements_2_new_vertices_graph2(graph2: Graph):
    m1 = PoseMeasurement(2, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(3, i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    elements = create_graph_elements(graph2, [cluster1, cluster2])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert len(elem1.new_vertices) == 1
    assert len(elem2.new_vertices) == 1

    assert e1 is not e2
    assert e1.index == 2
    assert e2.index == 3

    v1 = elem1.edge.vertices[0]
    v2 = elem2.edge.vertices[0]

    assert v1 is not v2
    assert v1 is not existing_v1 and v1 is not existing_v2
    assert v2 is not existing_v1 and v2 is not existing_v2
    assert v1.index == 2
    assert v2.index == 3
