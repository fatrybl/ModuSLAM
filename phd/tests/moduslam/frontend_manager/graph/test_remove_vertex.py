import gtsam
import pytest

from phd.measurements.processed_measurements import Imu as ImuMeasurement
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.measurements.processed_measurements import PoseOdometry as Odometry
from phd.moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from phd.moduslam.data_manager.batch_factory.readers.locations import Location
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.objects import (
    ImuCovariance,
    ImuData,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.new_element import GraphElement, NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.moduslam.setup_manager.sensors_factory.sensors import Imu as ImuSensor
from phd.moduslam.setup_manager.sensors_factory.sensors_configs import ImuConfig
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4, zero_vector3
from phd.moduslam.utils.exceptions import ValidationError


@pytest.fixture
def imu() -> ImuMeasurement:
    measurement = RawMeasurement(ImuSensor(ImuConfig(name="imu")), values=None)
    element = Element(0, measurement, Location())
    data = ImuData(zero_vector3, zero_vector3)
    covariance = ImuCovariance(identity3x3, identity3x3, identity3x3, identity3x3, identity3x3)
    return ImuMeasurement(element, data, covariance, identity4x4)


def test_remove_vertex_empty_graph():
    graph = Graph()
    v = PoseVertex(0)

    with pytest.raises(ValidationError):
        graph.remove_vertex(v)


def test_remove_vertex_with_1_edge():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, identity4x4, identity3x3, identity3x3, [])
    e = PriorPose(v, measurement, noise_model)
    element = GraphElement(e, new_vertices=[NewVertex(v, cluster, t)])

    graph.add_element(element)

    graph.remove_vertex(v)

    assert e not in graph.edges
    assert v not in graph.connections
    assert v not in graph.vertex_storage
    assert len(graph.edges) == 0
    assert graph.factor_graph.nrFactors() == 0


def test_remove_vertex_with_multiple_edges():
    t1, t2, t3 = 0, 1, 2
    graph = Graph()
    v1, v2, v3 = PoseVertex(0), PoseVertex(1), PoseVertex(2)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    measurement1 = Odometry(t2, TimeRange(t1, t2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = Odometry(t3, TimeRange(t1, t3), identity4x4, identity3x3, identity3x3, [])

    e1 = PoseOdometry(v1, v2, measurement1, noise_model)
    e2 = PoseOdometry(v1, v3, measurement2, noise_model)

    element1 = GraphElement(
        e1, new_vertices=[NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)]
    )
    element2 = GraphElement(e2, new_vertices=[NewVertex(v3, cluster3, t3)])

    graph.add_element(element1)
    graph.add_element(element2)

    graph.remove_vertex(v1)

    edges = graph.edges
    connections = graph.connections
    storage = graph.vertex_storage

    assert e1 not in edges and e2 not in edges
    assert v1 not in storage and v2 not in storage and v3 not in storage
    assert v1 not in connections and v2 not in connections and v3 not in connections
    assert len(graph.edges) == 0
    assert graph.factor_graph.nrFactors() == 0


def test_remove_vertex_in_cycle():
    t1, t2, t3 = 0, 1, 2
    graph = Graph()
    v1, v2, v3 = PoseVertex(t1), PoseVertex(t2), PoseVertex(t3)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    measurement1 = Odometry(t2, TimeRange(t1, t2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = Odometry(t3, TimeRange(t2, t3), identity4x4, identity3x3, identity3x3, [])
    measurement3 = Odometry(t3, TimeRange(t1, t3), identity4x4, identity3x3, identity3x3, [])

    e1 = PoseOdometry(v1, v2, measurement1, noise_model)
    e2 = PoseOdometry(v2, v3, measurement2, noise_model)
    e3 = PoseOdometry(v1, v3, measurement3, noise_model)

    element1 = GraphElement(
        e1, new_vertices=[NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)]
    )
    element2 = GraphElement(e2, new_vertices=[NewVertex(v3, cluster3, t3)])
    element3 = GraphElement(e3, new_vertices=[])

    graph.add_element(element1)
    graph.add_element(element2)
    graph.add_element(element3)

    graph.remove_vertex(v1)

    edges = graph.edges
    connections = graph.connections
    storage = graph.vertex_storage

    assert e1 not in edges and e3 not in edges
    assert e2 in edges
    assert v1 not in storage
    assert v2 in storage and v3 in storage
    assert v1 not in connections
    assert v2 in connections and v3 in connections
    assert len(graph.edges) == 1
    assert graph.factor_graph.nrFactors() == 1
