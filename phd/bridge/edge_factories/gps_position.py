import gtsam

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.noise_models import position_noise_model
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.measurements.processed_measurements import Gps
from phd.moduslam.frontend_manager.main_graph.edges.custom import GpsPosition
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose


class Factory(EdgeFactory):
    _vertex_type = Pose

    @classmethod
    def create(cls, graph: Graph, cluster: VertexCluster, measurement: Gps) -> GraphElement:
        """Create a new edge with GPS position factor.

        Args:
            graph: a main graph.

            cluster: a common cluster for new vertices.

            measurement: a GPS measurement.

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

        noise = position_noise_model(measurement.covariance)
        factor = gtsam.GPSFactor(vertex.backend_index, measurement.position, noise)
        edge = GpsPosition(vertex, measurement, factor, noise)

        if is_new_pose:
            new_vertices = {cluster: [(vertex, measurement.timestamp)]}
            element = GraphElement(edge, new_vertices)
        else:
            element = GraphElement(edge)

        return element
