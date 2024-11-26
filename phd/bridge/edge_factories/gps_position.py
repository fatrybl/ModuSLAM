from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.utils import (
    create_vertex_i_with_status,
    get_cluster,
    get_new_items,
)
from phd.measurements.processed_measurements import Gps
from phd.moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    covariance3x3_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity4x4


class Factory(EdgeFactory):
    _vertex_type = Pose

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: Gps
    ) -> GraphElement[GpsPosition]:
        """Create a new edge with GPS position factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a GPS measurement.

        Returns:
            a new element.
        """
        t = measurement.timestamp
        storage = graph.vertex_storage

        cluster = get_cluster(storage, clusters, t)

        pose = create_vertex_i_with_status(Pose, storage, cluster, t, identity4x4)

        noise_model = covariance3x3_noise_model(measurement.covariance)

        edge = GpsPosition(pose.instance, measurement, noise_model)

        new_vertices = get_new_items([pose])

        return GraphElement(edge, new_vertices)
