import gtsam.noiseModel
import pytest

from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4
from phd.utils.exceptions import ItemExistsError, ValidationError


def test_graph_element_no_validation_error():
    t = 0
    v1 = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)

    e = PriorPose(v1, measurement, noise_model)

    new_vertices = [NewVertex(v1, cluster, t)]

    GraphElement(e, new_vertices)


def test_graph_element_validation_error():
    t = 0
    v1, v2 = PoseVertex(t), PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)

    e = PriorPose(v1, measurement, noise_model)

    new_vertices = [NewVertex(v2, cluster, t)]

    with pytest.raises(ValidationError):
        GraphElement(e, new_vertices)


def test_graph_element_no_validation_error_with_empty_new_vertices():
    t = 0
    v1 = PoseVertex(t)
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)

    e = PriorPose(v1, measurement, noise_model)

    element = GraphElement(e)
    assert element is not None


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
