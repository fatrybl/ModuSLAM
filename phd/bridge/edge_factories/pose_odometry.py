import gtsam

from moduslam.frontend_manager.noise_models import pose_diagonal_noise_model
from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.external.objects.measurements import PseudoOdometry
from phd.moduslam.frontend_manager.main_graph.edges.custom import PoseOdometry
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
        cls, graph: Graph, cluster: VertexCluster, measurement: PseudoOdometry
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

        factor = gtsam.BetweenFactorPose3()
        noise = pose_diagonal_noise_model(measurement.variance)
        edge = PoseOdometry(pose_i, pose_j, measurement, factor, noise)

        new_vertices = {}
        if is_new_pose_i:
            new_vertices.update({cluster_i: [(pose_i, start)]})
        if is_new_pose_j:
            new_vertices.update({cluster_j: [(pose_j, stop)]})

        element = GraphElement(edge, new_vertices)
        return element
