import gtsam

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.noise_models import pose_block_diagonal_noise_model
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.custom import PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex


class Factory(EdgeFactory):
    _vertex_type = PoseVertex

    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement: PoseMeasurement
    ) -> GraphElement:
        """Creates a new edge with prior SE(3) pose factor.

        Args:
            graph: a main graph.

            cluster: a common cluster for new vertices.

            measurement: a pose SE(3) measurement.

        Returns:
            a new element.
        """
        is_new_pose = False
        pose = cluster.get_latest_vertex(cls._vertex_type)

        if pose:
            vertex = pose
        else:
            is_new_pose = True
            vertex = create_new_vertex(cls._vertex_type, graph)

        noise = pose_block_diagonal_noise_model(
            measurement.position_noise_covariance, measurement.orientation_noise_covariance
        )
        factor = gtsam.PriorFactorPose3(vertex.backend_index, measurement.pose, noise)
        edge = PriorPose(vertex, measurement, factor, noise)

        if is_new_pose:
            new_vertices = {cluster: [(vertex, measurement.timestamp)]}
            element = GraphElement(edge, new_vertices)
        else:
            element = GraphElement(edge)

        return element
