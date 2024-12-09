import gtsam
import pytest

from phd.external.metrics.candidate_connectivity import check_connectivity
from phd.measurements.processed import Pose as PoseMeasurement
from phd.measurements.processed import PoseOdometry as OdometryMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge, RadialEdge
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from phd.moduslam.utils.auxiliary_objects import identity4x4 as i4x4


class MultiVertexEdge(RadialEdge):
    """For testing purposes only."""

    def __init__(self, vertices: list[Vertex]):
        super().__init__()
        self._vertices = vertices

    @property
    def central_vertex(self) -> Vertex:
        return self._vertices[0]

    @property
    def radial_vertices(self) -> list[Vertex]:
        return self._vertices[1:]

    @property
    def vertices(self) -> list[Vertex]:
        return self._vertices

    @property
    def factor(self) -> gtsam.PriorFactorPose3:
        noise = gtsam.noiseModel.Isotropic.Sigma(6, 1)
        return gtsam.PriorFactorPose3(0, gtsam.Pose3(), noise)

    @property
    def measurement(self) -> PoseMeasurement:
        return PoseMeasurement(1, i4x4, i3x3, i3x3, [])


@pytest.fixture
def noise() -> gtsam.noiseModel.Isotropic:
    return gtsam.noiseModel.Isotropic.Sigma(6, 1)


@pytest.fixture
def measurement() -> OdometryMeasurement:
    return OdometryMeasurement(1, TimeRange(0, 1), i4x4, i3x3, i3x3, [])


def test_no_old_vertices(noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement):
    pose1, pose2 = Pose(0), Pose(1)
    edges: list[Edge] = [PoseOdometry(pose1, pose2, measurement, noise)]
    new_vertices: set[Vertex] = {pose1}
    old_vertices: set[Vertex] = set()

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_no_new_vertices(noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement):
    pose1, pose2 = Pose(0), Pose(1)
    edges: list[Edge] = [PoseOdometry(pose1, pose2, measurement, noise)]

    new_vertices: set[Vertex] = set()
    old_vertices: set[Vertex] = {pose1, pose2}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_no_vertices(noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement):
    pose1, pose2 = Pose(0), Pose(1)
    edges: list[Edge] = [PoseOdometry(pose1, pose2, measurement, noise)]
    new_vertices: set[Vertex] = set()
    old_vertices: set[Vertex] = set()

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_no_edges(noise: gtsam.noiseModel.Isotropic):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(3)
    edges: list[Edge] = []
    new_vertices: set[Vertex] = {pose2, pose3}
    old_vertices: set[Vertex] = {pose1}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is False


def test_connected_vertices(noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(3)
    edges: list[Edge] = [PoseOdometry(pose2, pose3, measurement, noise)]
    old_vertices: set[Vertex] = {pose1, pose2}
    new_vertices: set[Vertex] = {pose3}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_not_connected_vertices(
    noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement
):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(3)
    edges: list[Edge] = [PoseOdometry(pose1, pose2, measurement, noise)]
    old_vertices: set[Vertex] = {pose1, pose2}
    new_vertices: set[Vertex] = {pose3}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is False


def test_connected_vertices_with_unary_edges(noise: gtsam.noiseModel.Isotropic):
    pose1, pose2 = Pose(0), Pose(1)
    m = PoseMeasurement(1, i4x4, i3x3, i3x3, [])
    e1 = PriorPose(pose1, m, noise)
    e2 = PriorPose(pose2, m, noise)
    edges: list[Edge] = [e1, e2]
    old_vertices: set[Vertex] = {pose1}
    new_vertices: set[Vertex] = {pose2}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is False


def test_isolated_new_vertices(noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(2)
    edges: list[Edge] = [PoseOdometry(pose1, pose2, measurement, noise)]
    old_vertices: set[Vertex] = {pose1, pose2}
    new_vertices: set[Vertex] = {pose3}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is False


def test_multi_vertex_edge(noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(2)
    edges: list[Edge] = [MultiVertexEdge(vertices=[pose1, pose2, pose3])]
    old_vertices: set[Vertex] = {pose1}
    new_vertices: set[Vertex] = {pose2, pose3}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_multi_vertex_edge_no_old_vertices(
    noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement
):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(2)
    edges: list[Edge] = [MultiVertexEdge(vertices=[pose1, pose2, pose3])]
    old_vertices: set[Vertex] = set()
    new_vertices: set[Vertex] = {pose1, pose2, pose3}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_multi_vertex_edge_no_new_vertices(
    noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement
):
    pose1, pose2, pose3 = Pose(0), Pose(1), Pose(2)
    edges: list[Edge] = [MultiVertexEdge(vertices=[pose1, pose2, pose3])]
    old_vertices: set[Vertex] = {pose1, pose2, pose3}
    new_vertices: set[Vertex] = set()

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_2_multi_vertex_edges_connected(
    noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement
):
    pose1, pose2, pose3, pose4 = Pose(0), Pose(1), Pose(2), Pose(3)
    e1 = MultiVertexEdge(vertices=[pose1, pose2])
    e2 = MultiVertexEdge(vertices=[pose3, pose4])
    edges: list[Edge] = [e1, e2]
    old_vertices: set[Vertex] = {pose1, pose3}
    new_vertices: set[Vertex] = {pose2, pose4}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is True


def test_2_multi_vertex_edges_not_connected_1(
    noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement
):
    pose1, pose2, pose3, pose4 = Pose(0), Pose(1), Pose(2), Pose(3)
    e1 = MultiVertexEdge(vertices=[pose1, pose2])
    e2 = MultiVertexEdge(vertices=[pose3, pose4])
    edges: list[Edge] = [e1, e2]
    old_vertices: set[Vertex] = {pose1, pose2}
    new_vertices: set[Vertex] = {pose3, pose4}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is False


def test_2_multi_vertex_edges_not_connected_2(
    noise: gtsam.noiseModel.Isotropic, measurement: OdometryMeasurement
):
    pose1, pose2, pose3, pose4 = Pose(0), Pose(1), Pose(2), Pose(3)
    e1 = MultiVertexEdge(vertices=[pose1, pose2])
    e2 = MultiVertexEdge(vertices=[pose3, pose4])
    edges: list[Edge] = [e1, e2]
    old_vertices: set[Vertex] = {pose1}
    new_vertices: set[Vertex] = {pose2, pose4}

    connectivity = check_connectivity(edges, old_vertices, new_vertices)

    assert connectivity is False
