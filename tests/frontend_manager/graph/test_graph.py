"""Tests for the Graph class."""

import gtsam
import numpy as np
import pytest
from gtsam import PriorFactorPoint2
from gtsam.noiseModel import Diagonal

from moduslam.frontend_manager.graph.base_edges import UnaryEdge
from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.graph.graph import Graph

noise = Diagonal.Sigmas([1, 1])


@pytest.fixture
def graph():
    return Graph()


@pytest.fixture
def edge():
    return UnaryEdge(
        Pose(),
        measurements=(),
        noise_model=noise,
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=noise),
    )


@pytest.fixture
def edges():
    v1, v2, v3 = Pose(index=0), Pose(index=1), Pose(index=2)

    e1 = UnaryEdge(
        v1,
        measurements=(),
        noise_model=noise,
        factor=PriorFactorPoint2(key=0, prior=[0, 0], noiseModel=noise),
    )

    e2 = UnaryEdge(
        v2,
        measurements=(),
        noise_model=noise,
        factor=PriorFactorPoint2(key=1, prior=[1, 1], noiseModel=noise),
    )

    e3 = UnaryEdge(
        v3,
        measurements=(),
        noise_model=noise,
        factor=PriorFactorPoint2(key=2, prior=[1, 1], noiseModel=noise),
    )
    return e1, e2, e3


class TestGraph:
    """
    TODO: add more test cases for Graph.update method.
          now it only works with OptimizableVertex.
    """

    def test_add_edge(self, graph: Graph, edge: UnaryEdge):
        graph.add_edge(edge)
        assert edge in graph.edge_storage.edges

    def test_add_edges(self, graph: Graph, edges: tuple[UnaryEdge, ...]):
        graph.add_edges(edges)
        assert len(graph.edge_storage.edges) == len(edges)
        assert all(e in graph.edge_storage.edges for e in edges)

    def test_remove_edge(self, graph: Graph, edge: UnaryEdge):
        graph.add_edge(edge)
        graph.remove_edge(edge)
        assert edge not in graph.edge_storage.edges

    def test_remove_edges(self, graph: Graph, edges: tuple[UnaryEdge, ...]):
        graph.add_edges(edges)
        graph.remove_edges(edges)
        assert len(graph.edge_storage.edges) == 0

    def test_remove_vertex(self, graph: Graph, edge: UnaryEdge):
        graph.add_edge(edge)
        vertices = edge.all_vertices
        vertex = list(vertices)[0]
        graph.remove_vertex(vertex)
        assert vertex not in graph.vertex_storage.vertices

    def test_remove_vertices(self, graph: Graph, edges: tuple[UnaryEdge, ...]):
        graph.add_edges(edges)
        vertices = [v for e in edges for v in e.all_vertices]
        graph.remove_vertices(vertices)
        assert len(graph.vertex_storage.vertices) == 0

    def test_update(self, graph: Graph, edge: UnaryEdge):
        new_pose = gtsam.Pose3(gtsam.Rot3((10, 10, 10)), (10, 10, 10))
        graph.add_edge(edge)
        vertex: Pose = list(graph.vertex_storage.vertices)[0]

        values = gtsam.Values()
        values.insert(vertex.gtsam_index, new_pose)
        graph.update(values)

        assert np.array_equal(vertex.value, new_pose.matrix())

    def test_gtsam_values(self, graph: Graph, edge: UnaryEdge):
        new_pose = gtsam.Pose3(gtsam.Rot3((10, 10, 10)), (10, 10, 10))
        values = gtsam.Values()

        graph.add_edge(edge)

        vertex: Pose = list(graph.vertex_storage.vertices)[0]
        values.insert(vertex.gtsam_index, new_pose)
        graph.update(values)

        pose: gtsam.Pose3 = graph.gtsam_values.atPose3(vertex.gtsam_index)
        assert pose.equals(new_pose, 1e-9)
