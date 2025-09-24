from moduslam.bridge.edge_factories.factory_protocol import EdgeFactory
from moduslam.bridge.edge_factories.utils import (
    create_new_vertices,
    create_vertex_i_with_status,
    get_cluster,
)
from moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from moduslam.frontend_manager.main_graph.edges.noise_models import (
    huber_diagonal_noise_model,
)
from moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.measurement_storage.measurements.position import Position
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_objects import identity4x4


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: Position
    ) -> GraphElement[GpsPosition]:
        """Create a new edge with the GPS position factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a GPS measurement.

        Returns:
            a new element.
        """
        huber_loss_trh = 1.0
        t = measurement.timestamp
        storage = graph.vertex_storage

        cluster = get_cluster(storage, clusters, t)

        pose = create_vertex_i_with_status(Pose, storage, cluster, t, identity4x4)

        cov = measurement.covariance
        variances = (cov[0][0], cov[1][1], cov[2][2])
        noise_model = huber_diagonal_noise_model(variances, huber_loss_trh)

        edge = GpsPosition(pose.instance, measurement, noise_model)

        new_vertices = create_new_vertices([pose])

        return GraphElement(edge, {pose.instance: t}, new_vertices)
