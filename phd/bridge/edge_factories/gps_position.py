from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.measurements.processed_measurements import Gps
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Factory(EdgeFactory):
    _vertex_type = Pose

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: Gps
    ) -> GraphElement:
        """Create a new edge with GPS position factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a GPS measurement.

        Returns:
            a new element.
        """
        # is_new_pose = False
        # pose = cluster.get_latest_vertex(cls._vertex_type)
        #
        # if pose:
        #     vertex = pose
        # else:
        #     is_new_pose = True
        #     vertex = create_new_vertex(cls._vertex_type, graph)
        #
        # noise = covariance3x3_noise_model(measurement.covariance)
        # factor = gtsam.GPSFactor(vertex.backend_index, measurement.position, noise)
        # edge = GpsPosition(vertex, measurement, factor, noise)
        #
        # if is_new_pose:
        #     new_vertices = {cluster: [(vertex, measurement.timestamp)]}
        #     element = GraphElement(edge, new_vertices)
        # else:
        #     element = GraphElement(edge)
        #
        # return element
        raise NotImplementedError
