import gtsam.noiseModel
import pytest

from phd.measurement_storage.measurements.imu import (
    ContinuousImu,
    ImuCovariance,
    ImuData,
)
from phd.measurement_storage.measurements.imu import ProcessedImu as ImuMeasurement
from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.measurement_storage.measurements.pose_odometry import (
    Odometry as OdometryMeasurement,
)
from phd.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias as ImuBiasVertex,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity as VelocityVertex,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4, zero_vector3
from phd.moduslam.utils.exceptions import ValidationError


@pytest.fixture
def imu() -> ImuMeasurement:
    data = ImuData(zero_vector3, zero_vector3)
    covariance = ImuCovariance(identity3x3, identity3x3, identity3x3, identity3x3, identity3x3)
    return ImuMeasurement(0, data, covariance, identity4x4)


def test_remove_existing_edge():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, identity4x4, identity3x3, identity3x3)
    e = PriorPose(v, measurement, noise_model)

    element = GraphElement(edge=e, new_vertices=[NewVertex(v, cluster, t)])

    graph.add_element(element)

    graph.remove_edge(e)

    assert e not in graph.edges
    assert len(graph.edges) == 0
    assert v not in graph.connections
    assert graph.factor_graph.nrFactors() == 0


def test_remove_nonexistent_edge():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, identity4x4, identity3x3, identity3x3)
    e = PriorPose(v, measurement, noise_model)

    with pytest.raises(ValidationError):
        graph.remove_edge(e)


def test_remove_edge_invalid_index():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(t, identity4x4, identity3x3, identity3x3)
    e = PriorPose(v, measurement, noise_model)
    element = GraphElement(e, [NewVertex(v, cluster, t)])

    graph.add_element(element)

    e.index = 100500

    with pytest.raises(ValidationError):
        graph.remove_edge(e)


def test_remove_edge_with_multiple_vertices():
    graph = Graph()
    t1, t2 = 0, 1
    t_range = TimeRange(t1, t2)
    v1, v2 = PoseVertex(t1), PoseVertex(t2)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = OdometryMeasurement(t1, t_range, identity4x4, identity3x3, identity3x3)
    e = PoseOdometry(v1, v2, measurement, noise_model)

    element = GraphElement(e, [NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)])
    graph.add_element(element)

    graph.remove_edge(e)

    assert e not in graph.edges
    assert v1 not in graph.connections
    assert v2 not in graph.connections
    assert v1 not in graph.vertex_storage
    assert v2 not in graph.vertex_storage
    assert graph.factor_graph.nrFactors() == 0


def test_remove_specific_edge_from_multiple():
    graph = Graph()
    t1, t2, t3 = 0, 1, 2
    v1, v2, v3 = PoseVertex(t1), PoseVertex(t2), PoseVertex(t3)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    m1 = OdometryMeasurement(t1, TimeRange(t1, t2), identity4x4, identity3x3, identity3x3)
    m2 = OdometryMeasurement(t2, TimeRange(t2, t3), identity4x4, identity3x3, identity3x3)

    edge1 = PoseOdometry(v1, v2, m1, noise_model)
    edge2 = PoseOdometry(v2, v3, m2, noise_model)

    element1 = GraphElement(edge1, [NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)])
    element2 = GraphElement(edge2, [NewVertex(v3, cluster3, t3)])

    graph.add_elements([element1, element2])

    graph.remove_edge(edge1)

    assert edge1 not in graph.edges
    assert edge2 in graph.edges
    assert v1 not in graph.connections
    assert v2 in graph.connections
    assert v3 in graph.connections
    assert v1 not in graph.vertex_storage
    assert v2 in graph.vertex_storage
    assert v3 in graph.vertex_storage
    assert cluster1 not in graph.vertex_storage.clusters
    assert graph.edges.first == graph.edges.last == edge2
    assert graph.factor_graph.nrFactors() == len(graph.edges) == 1


def test_remove_edge_updates_factor_graph():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(t, identity4x4, identity3x3, identity3x3)
    e = PriorPose(v, measurement, noise_model)

    element = GraphElement(e, [NewVertex(v, cluster, t)])
    graph.add_element(element)

    initial_factor_count = graph.factor_graph.nrFactors()
    graph.remove_edge(e)
    updated_factor_count = graph.factor_graph.nrFactors()

    assert updated_factor_count == initial_factor_count - 1


def test_remove_edge_with_single_vertex_removes_vertex():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(t, identity4x4, identity3x3, identity3x3)
    e = PriorPose(v, measurement, noise_model)

    element = GraphElement(e, [NewVertex(v, cluster, t)])
    graph.add_element(element)

    graph.remove_edge(e)

    assert e not in graph.edges
    assert v not in graph.connections
    assert v not in graph.vertex_storage
    assert graph.factor_graph.nrFactors() == 0
    assert len(graph.edges) == 0
    assert len(graph.connections) == 0
    assert len(graph.vertex_storage.vertices) == 0
    assert len(graph.vertex_storage.clusters) == 0


def test_remove_edge_with_duplicate_vertices():
    graph = Graph()
    t1, t2 = 0, 1
    v = PoseVertex(t1)
    cluster1 = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    measurement1 = PoseMeasurement(t1, identity4x4, identity3x3, identity3x3)
    measurement2 = PoseMeasurement(t2, identity4x4, identity3x3, identity3x3)
    edge1 = PriorPose(v, measurement1, noise_model)
    edge2 = PriorPose(v, measurement2, noise_model)

    element1 = GraphElement(edge1, [NewVertex(v, cluster1, t1)])
    element2 = GraphElement(edge2, [])

    graph.add_elements([element1, element2])

    graph.remove_edge(edge1)

    assert edge1 not in graph.edges
    assert edge2 in graph.edges
    assert v in graph.connections
    assert v in graph.vertex_storage
    assert edge2 in graph.connections[v]
    assert graph.factor_graph.nrFactors() == 1
    assert len(graph.edges) == 1


def test_remove_edge_with_vertex_in_cluster_updates_cluster():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(t, identity4x4, identity3x3, identity3x3)
    e = PriorPose(v, measurement, noise_model)

    element = GraphElement(e, [NewVertex(v, cluster, t)])
    graph.add_element(element)

    assert v in cluster.vertices

    graph.remove_edge(e)

    assert e not in graph.edges

    assert v not in cluster.vertices
    assert v not in graph.connections
    assert v not in graph.vertex_storage
    assert graph.factor_graph.nrFactors() == 0


def test_remove_3_edges(imu: ImuMeasurement):
    graph = Graph()
    t1, t2, t3 = 0, 1, 2
    p1, p2, p3 = PoseVertex(0), PoseVertex(1), PoseVertex(2)
    v1, v2 = VelocityVertex(0), VelocityVertex(1)
    b1, b2 = ImuBiasVertex(0), ImuBiasVertex(1)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    m1 = OdometryMeasurement(t1, TimeRange(t1, t2), identity4x4, identity3x3, identity3x3)
    m2 = OdometryMeasurement(t2, TimeRange(t2, t3), identity4x4, identity3x3, identity3x3)
    m3 = OdometryMeasurement(t2, TimeRange(t1, t3), identity4x4, identity3x3, identity3x3)
    m4 = ContinuousImu([imu], start=t1, stop=t3)

    gravity = (9.81, 0, 0)
    params = gtsam.PreintegrationCombinedParams(gravity)
    pim = gtsam.PreintegratedCombinedMeasurements(params)

    edge1 = PoseOdometry(p1, p2, m1, noise_model)
    edge2 = PoseOdometry(p2, p3, m2, noise_model)
    edge3 = PoseOdometry(p1, p3, m3, noise_model)
    edge4 = ImuOdometry(p1, v1, b1, p3, v2, b2, m4, pim)

    element1 = GraphElement(edge1, [NewVertex(p1, cluster1, t1), NewVertex(p2, cluster2, t2)])
    element2 = GraphElement(edge2, [NewVertex(p3, cluster3, t3)])
    element3 = GraphElement(edge3, [])
    element4 = GraphElement(
        edge4,
        [
            NewVertex(v1, cluster1, t1),
            NewVertex(v2, cluster3, t3),
            NewVertex(b1, cluster1, t1),
            NewVertex(b2, cluster3, t3),
        ],
    )

    graph.add_elements([element1, element2, element3, element4])

    graph.remove_edge(edge4)

    assert edge4 not in graph.edges
    assert v1 not in graph.vertex_storage
    assert v2 not in graph.vertex_storage
    assert b1 not in graph.vertex_storage
    assert b2 not in graph.vertex_storage
    assert v1 not in graph.connections
    assert v2 not in graph.connections
    assert b1 not in graph.connections
    assert b2 not in graph.connections
    assert graph.factor_graph.nrFactors() == 3

    graph.remove_edge(edge1)
    graph.remove_edge(edge2)

    assert edge1 not in graph.edges
    assert edge2 not in graph.edges
    assert p1 in graph.vertex_storage
    assert p3 in graph.vertex_storage
    assert p2 not in graph.vertex_storage
    assert graph.factor_graph.nrFactors() == 1
