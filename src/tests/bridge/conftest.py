import pytest

from src.bridge.distributor import distribution_table
from src.bridge.edge_factories.pose_odometry import Factory
from src.measurement_storage.measurements.imu import (
    ContinuousImu,
    ImuCovariance,
    ImuData,
    ProcessedImu,
)
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.measurement_storage.storage import MeasurementStorage
from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.edges.noise_models import (
    se3_isotropic_noise_model,
)
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.auxiliary_objects import one_vector3


@pytest.fixture(scope="module", autouse=True)
def add_factory_to_table():
    """Add the tested factory to the table of measurements` types and edge factories."""
    distribution_table.update({Odometry: Factory})


@pytest.fixture()
def clean_storage() -> None:
    """Clears the measurement storage."""
    MeasurementStorage.clear()


@pytest.fixture
def graph0() -> Graph:
    """Empty graph."""
    return Graph()


@pytest.fixture
def graph1() -> Graph:
    """Graph with one pose."""
    graph = Graph()
    t = 0
    v = Pose(0)
    noise = se3_isotropic_noise_model(1)
    m = PoseMeasurement(t, i4x4, i3x3, i3x3)
    edge1 = PriorPose(v, m, noise)
    cluster = VertexCluster()
    element1 = GraphElement(edge1, {v: t}, (NewVertex(v, cluster, t),))
    graph.add_element(element1)
    return graph


@pytest.fixture
def graph2() -> Graph:
    """Graph with two poses."""
    graph = Graph()
    t1, t2 = 0, 1
    v1, v2 = Pose(0), Pose(1)
    noise = se3_isotropic_noise_model(1)
    m1, m2 = PoseMeasurement(t1, i4x4, i3x3, i3x3), PoseMeasurement(t2, i4x4, i3x3, i3x3)
    edge1, edge2 = PriorPose(v1, m1, noise), PriorPose(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, {v1: t1}, (NewVertex(v1, cluster1, t1),))
    element2 = GraphElement(edge2, {v2: t2}, (NewVertex(v2, cluster2, t2),))
    graph.add_elements([element1, element2])
    return graph


@pytest.fixture
def measurement() -> ContinuousImu[ProcessedImu]:
    """Continuous IMU measurement with 3 raw measurements"""
    t1, t2 = 0, 3
    data = ImuData(one_vector3, one_vector3)
    cov = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
    imu1 = ProcessedImu(0, data, cov, i4x4)
    imu2 = ProcessedImu(1, data, cov, i4x4)
    imu3 = ProcessedImu(2, data, cov, i4x4)
    return ContinuousImu([imu1, imu2, imu3], start=t1, stop=t2)
