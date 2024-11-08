import gtsam
import numpy as np

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.noise_models import pose_block_diagonal_noise_model
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.measurements.processed_measurements import PoseOdometry as OdometryMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.custom import (
    PoseOdometry as OdometryEdge,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement: OdometryMeasurement
    ) -> GraphElement:
        """Creates a new edge with pose-based odometry factor."""
        start = measurement.time_range.start
        stop = measurement.time_range.stop

        is_new_pose_i = False
        is_new_pose_j = False

        cluster_i = graph.vertex_storage.get_cluster(start)
        cluster_j = cluster

        if cluster_i:
            pose = cluster.get_latest_vertex(cls._vertex_type)
            if pose:
                pose_i = pose
            else:
                is_new_pose_i = True
                pose_i = create_new_vertex(cls._vertex_type, graph)
        else:
            cluster_i = VertexCluster()
            is_new_pose_i = True
            pose_i = create_new_vertex(cls._vertex_type, graph)

        pose_j = cluster_j.get_latest_vertex(cls._vertex_type)
        if not pose_j:
            is_new_pose_j = True
            pose_j = create_new_vertex(cls._vertex_type, graph)

        new_vertices = {}
        if is_new_pose_i:
            new_vertices.update({cluster_i: [(pose_i, start)]})
        if is_new_pose_j:
            new_vertices.update({cluster_j: [(pose_j, stop)]})

        edge = cls._create_edge(pose_i, pose_j, measurement)

        element = GraphElement(edge, new_vertices)
        return element

    @classmethod
    def _create_edge(
        cls, pose_i: Pose, pose_j: Pose, measurement: OdometryMeasurement
    ) -> OdometryEdge:
        """Creates a PoseOdometry edge.

        Args:
            pose_i: initial pose vertex.

            pose_j: final pose vertex.

            measurement: odometry measurement.

        Returns:
            new PoseOdometry edge.
        """

        noise = pose_block_diagonal_noise_model(
            measurement.position_covariance, measurement.orientation_covariance
        )

        d_pose = np.array(measurement.pose)
        factor = gtsam.BetweenFactorPose3(pose_i.backend_index, pose_j.backend_index, d_pose, noise)
        edge = OdometryEdge(pose_i, pose_j, measurement, factor, noise)
        return edge
