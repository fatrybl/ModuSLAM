"""Tests for both GraphElement and NewVertex classes."""

import pytest
from gtsam.noiseModel import Isotropic

from moduslam.frontend_manager.main_graph.data_classes import NewVertex
from moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from moduslam.frontend_manager.main_graph.graph import GraphElement
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from moduslam.measurement_storage.measurements.pose import Pose as PoseMeasurement
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4
from moduslam.utils.exceptions import ItemExistsError, ValidationError


def test_no_validation_error(noise: Isotropic):
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise)
    new = NewVertex(v, cluster, t)

    element = GraphElement(e, {v: t}, (new,))

    assert element.edge == e
    assert element.vertex_timestamp_table == {v: t}
    assert element.new_vertices == (new,)


def test_empty_new_vertices(noise: Isotropic):
    t = 0
    v = PoseVertex(t)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise)

    element = GraphElement(e, {v: t}, ())

    assert element.edge == e
    assert element.vertex_timestamp_table == {v: t}
    assert element.new_vertices == ()


def test_new_vertex_not_in_edge(noise: Isotropic):
    t = 0
    v1, v2 = PoseVertex(t), PoseVertex(t)
    cluster = VertexCluster()
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v1, measurement, noise)
    new = NewVertex(v2, cluster, t)

    with pytest.raises(ValidationError):
        _ = GraphElement(e, {v1: t, v2: t}, (new,))


def test_edge_vertices_table_vertices_missmatch(noise: Isotropic):
    t = 0
    v1, v2 = PoseVertex(t), PoseVertex(t)
    cluster = VertexCluster()
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v1, measurement, noise)
    new = NewVertex(v1, cluster, t)

    with pytest.raises(ValidationError):
        _ = GraphElement(e, {v2: t}, (new,))


def test_negative_timestamp_in_table(noise: Isotropic):
    t1, t2 = 0, -1
    v = PoseVertex(t1)
    cluster = VertexCluster()
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise)
    new = NewVertex(v, cluster, t1)

    with pytest.raises(ValidationError):
        _ = GraphElement(e, {v: t2}, (new,))


def test_new_vertex_item_exists_error():
    t = 0
    v = Pose(0)
    cluster = VertexCluster()
    cluster.add(v, t)

    with pytest.raises(ItemExistsError):
        NewVertex(v, cluster, t)


def test_new_vertex_creation_success():
    t = 0
    v = Pose(0)
    cluster = VertexCluster()

    new_vertex = NewVertex(v, cluster, t)

    assert new_vertex.instance == v
    assert new_vertex.cluster == cluster
    assert new_vertex.timestamp == t
    assert new_vertex.instance not in new_vertex.cluster
