"""Tests for the Graph class.

TODO: add more test cases for Graph.update method.
      now it only works with OptimizableVertex.
"""

import gtsam
import numpy as np
import pytest
from gtsam import PriorFactorPoint2
from gtsam.noiseModel import Diagonal

from moduslam.frontend_manager.graph.base_edges import MultiEdge, UnaryEdge
from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.measurement_storage import Measurement
from tests.frontend_manager.conftest import measurement

noise = Diagonal.Sigmas([1, 1])


@pytest.fixture
def graph():
    return Graph()


@pytest.fixture
def edge(measurement):
    return UnaryEdge(
        Pose(),
        measurement=measurement,
        noise_model=noise,
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=noise),
    )


@pytest.fixture
def multi_edge(measurement):
    camera_params = gtsam.Cal3_S2(1, 1, 0, 0, 0)
    return MultiEdge(
        vertices=[Pose()],
        measurements=[measurement],
        factor=gtsam.SmartProjectionPose3Factor(noise, camera_params),
        noise_model=noise,
    )


@pytest.fixture
def edges(measurement):
    v1, v2, v3 = Pose(index=0), Pose(index=1), Pose(index=2)

    e1 = UnaryEdge(
        v1,
        measurement=measurement,
        noise_model=noise,
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=noise),
    )

    e2 = UnaryEdge(
        v2,
        measurement=measurement,
        noise_model=noise,
        factor=PriorFactorPoint2(key=1, prior=[1, 1], noiseModel=noise),
    )

    e3 = UnaryEdge(
        v3,
        measurement=measurement,
        noise_model=noise,
        factor=PriorFactorPoint2(key=2, prior=[1, 1], noiseModel=noise),
    )
    return e1, e2, e3


def test_add_edge(graph: Graph, edge: UnaryEdge):
    graph.add_edge(edge)
    assert edge in graph.edge_storage.edges


def test_add_edges(graph: Graph, edges: tuple[UnaryEdge, ...]):
    graph.add_edges(edges)
    assert len(graph.edge_storage.edges) == len(edges)
    assert all(e in graph.edge_storage.edges for e in edges)


def test_remove_edge(graph: Graph, edge: UnaryEdge):
    graph.add_edge(edge)
    graph.remove_edge(edge)
    assert edge not in graph.edge_storage.edges


def test_remove_edges(graph: Graph, edges: tuple[UnaryEdge, ...]):
    graph.add_edges(edges)
    graph.remove_edges(edges)
    assert len(graph.edge_storage.edges) == 0


def test_remove_vertex(graph: Graph, edge: UnaryEdge):
    graph.add_edge(edge)
    vertices = edge.vertices
    vertex = list(vertices)[0]
    graph.remove_vertex(vertex)
    assert vertex not in graph.vertex_storage.vertices
    assert len(graph.get_connected_edges(vertex)) == 0


def test_remove_vertices(graph: Graph, edges: tuple[UnaryEdge, ...]):
    graph.add_edges(edges)
    vertices = [v for e in edges for v in e.vertices]
    graph.remove_vertices(vertices)
    assert len(graph.vertex_storage.vertices) == 0
    assert len(graph.edge_storage.edges) == 0


def test_update_edge_add_new_vertex(graph: Graph, multi_edge: MultiEdge, measurement: Measurement):
    graph.add_edge(multi_edge)
    original_vertices = set(multi_edge.vertices)
    new_pose = Pose()

    multi_edge.vertices.append(new_pose)
    multi_edge.measurements.append(measurement)
    graph.update_connections(original_vertices, multi_edge)

    assert new_pose in graph.vertex_storage.vertices
    assert multi_edge in graph.edge_storage.edges
    assert multi_edge in graph.get_connected_edges(new_pose)


def test_update_edge_remove_vertex(graph: Graph, multi_edge: MultiEdge, measurement: Measurement):
    original_vertices = set(multi_edge.vertices)

    graph.add_edge(multi_edge)
    removed_vertex = multi_edge.vertices.pop()
    multi_edge.measurements.pop()
    graph.update_connections(original_vertices, multi_edge)

    assert removed_vertex in graph.vertex_storage.vertices
    assert multi_edge in graph.edge_storage.edges
    assert multi_edge not in graph.get_connected_edges(removed_vertex)


def test_update(graph: Graph, edge: UnaryEdge):
    new_pose = gtsam.Pose3(gtsam.Rot3.Ypr(1, 1, 1), (1, 1, 1))
    graph.add_edge(edge)
    vertex: Pose = list(graph.vertex_storage.vertices)[0]

    values = gtsam.Values()
    values.insert(vertex.backend_index, new_pose)
    graph.update(values)

    assert np.array_equal(vertex.value, new_pose.matrix())


def test_backend_values(graph: Graph, edge: UnaryEdge):
    new_pose = gtsam.Pose3(gtsam.Rot3((10, 10, 10)), (10, 10, 10))
    values = gtsam.Values()

    graph.add_edge(edge)

    vertex: Pose = list(graph.vertex_storage.vertices)[0]
    values.insert(vertex.backend_index, new_pose)
    graph.update(values)

    pose: gtsam.Pose3 = graph.backend_values.atPose3(vertex.backend_index)
    assert pose.equals(new_pose, 1e-9)
