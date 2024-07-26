"""Tests for VertexStorage class.

TODO: add tests for update_non_optimizable_vertices methods.
"""

import gtsam
import numpy as np
import pytest

from moduslam.frontend_manager.graph.custom_vertices import Feature3D, Pose
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage


@pytest.fixture
def vertex_storage():
    return VertexStorage()


@pytest.fixture
def optimizable_vertex():
    return Pose()


@pytest.fixture
def non_optimizable_vertex():
    return Feature3D()


def test_add(
    vertex_storage: VertexStorage,
    optimizable_vertex: Pose,
    non_optimizable_vertex: Feature3D,
):
    vertex_storage.add(optimizable_vertex)
    assert optimizable_vertex in vertex_storage.vertices
    assert optimizable_vertex in vertex_storage.optimizable_vertices
    assert len(vertex_storage.get_vertices(type(optimizable_vertex))) == 1

    vertex_storage.add(non_optimizable_vertex)
    assert non_optimizable_vertex in vertex_storage.vertices
    assert non_optimizable_vertex in vertex_storage.not_optimizable_vertices
    assert len(vertex_storage.get_vertices(type(non_optimizable_vertex))) == 1


def test_add_multiple(vertex_storage, optimizable_vertex, non_optimizable_vertex):
    vertex_storage.add([optimizable_vertex, non_optimizable_vertex])

    assert optimizable_vertex in vertex_storage.vertices
    assert optimizable_vertex in vertex_storage.optimizable_vertices
    assert len(vertex_storage.get_vertices(type(optimizable_vertex))) == 1

    assert non_optimizable_vertex in vertex_storage.vertices
    assert non_optimizable_vertex in vertex_storage.not_optimizable_vertices
    assert len(vertex_storage.get_vertices(type(non_optimizable_vertex))) == 1

    assert optimizable_vertex not in vertex_storage.not_optimizable_vertices
    assert non_optimizable_vertex not in vertex_storage.optimizable_vertices

    assert len(vertex_storage.vertices) == 2


def test_remove(vertex_storage, optimizable_vertex, non_optimizable_vertex):
    vertex_storage.add(optimizable_vertex)
    vertex_storage.remove(optimizable_vertex)

    assert optimizable_vertex not in vertex_storage.vertices
    assert optimizable_vertex not in vertex_storage.optimizable_vertices
    assert optimizable_vertex not in vertex_storage.not_optimizable_vertices
    assert len(vertex_storage.get_vertices(type(optimizable_vertex))) == 0

    vertex_storage.add(non_optimizable_vertex)
    vertex_storage.remove(non_optimizable_vertex)

    assert non_optimizable_vertex not in vertex_storage.vertices
    assert non_optimizable_vertex not in vertex_storage.optimizable_vertices
    assert non_optimizable_vertex not in vertex_storage.not_optimizable_vertices
    assert len(vertex_storage.get_vertices(type(optimizable_vertex))) == 0


def test_remove_multiple(vertex_storage, optimizable_vertex, non_optimizable_vertex):
    vertex_storage.add([optimizable_vertex, non_optimizable_vertex])
    vertex_storage.remove([optimizable_vertex, non_optimizable_vertex])

    assert optimizable_vertex not in vertex_storage.vertices
    assert optimizable_vertex not in vertex_storage.optimizable_vertices
    assert optimizable_vertex not in vertex_storage.not_optimizable_vertices
    assert len(vertex_storage.get_vertices(type(optimizable_vertex))) == 0

    assert non_optimizable_vertex not in vertex_storage.vertices
    assert non_optimizable_vertex not in vertex_storage.optimizable_vertices
    assert non_optimizable_vertex not in vertex_storage.not_optimizable_vertices
    assert len(vertex_storage.get_vertices(type(optimizable_vertex))) == 0


def test_get_vertices(vertex_storage, optimizable_vertex, non_optimizable_vertex):
    vertex_storage.add(optimizable_vertex)
    vertex_storage.add(non_optimizable_vertex)
    assert optimizable_vertex in vertex_storage.get_vertices(type(optimizable_vertex))
    assert non_optimizable_vertex in vertex_storage.get_vertices(type(non_optimizable_vertex))


def test_get_last_vertex(vertex_storage, optimizable_vertex, non_optimizable_vertex):
    vertex_storage.add(optimizable_vertex)
    assert vertex_storage.get_last_vertex(type(optimizable_vertex)) == optimizable_vertex
    vertex_storage.add(non_optimizable_vertex)
    assert vertex_storage.get_last_vertex(type(non_optimizable_vertex)) == non_optimizable_vertex


def test_update_optimizable_vertex(vertex_storage, optimizable_vertex: Pose):
    vertex_storage.add(optimizable_vertex)
    pose = gtsam.Pose3(gtsam.Rot3([10, 10, 10]), np.array([10, 10, 10]))
    values = gtsam.Values()

    values.insert(optimizable_vertex.backend_index, pose)

    vertex_storage.update_optimizable_vertices(values)
    vertex: Pose = vertex_storage.get_last_vertex(Pose)

    assert np.array_equal(vertex.rotation, pose.rotation().matrix(), equal_nan=True) is True
    assert np.array_equal(vertex.position, pose.translation()) is True


@pytest.mark.skip(reason="Not implemented")
def test_update_non_optimizable_vertex(vertex_storage, non_optimizable_vertex: Feature3D):
    vertex_storage.add(non_optimizable_vertex)

    new_values: dict[Feature3D, np.ndarray] = {non_optimizable_vertex: np.array([10, 10, 10])}

    vertex_storage.update_not_optimizable_vertices()
    vertex = vertex_storage.get_last_vertex(Feature3D)

    assert np.array_equal(vertex.position, new_values[non_optimizable_vertex]) is True
