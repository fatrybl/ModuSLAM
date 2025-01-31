from src.bridge.edge_factories.factory_protocol import EdgeFactory
from src.bridge.edge_factories.utils import (
    create_new_vertices,
    create_vertex_i_with_status,
    get_cluster,
)
from src.measurement_storage.measurements.imu_bias import Bias as BiasMeasurement
from src.moduslam.frontend_manager.main_graph.edges.imu_bias import ImuBias as PriorBias
from src.moduslam.frontend_manager.main_graph.edges.noise_models import (
    variance_6d,
)
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import ImuBias
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import zero_vector3


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: BiasMeasurement
    ) -> GraphElement[PriorBias]:
        """Creates a new edge with prior IMU bias factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: an angular velocity and linear acceleration initial biases.

        Returns:
            a new element.
        """
        t = measurement.timestamp
        storage = graph.vertex_storage

        cluster = get_cluster(storage, clusters, t)
        default_bias = (zero_vector3, zero_vector3)
        bias = create_vertex_i_with_status(ImuBias, storage, cluster, t, default_bias)

        cov1 = measurement.linear_acceleration_noise_covariance
        cov2 = measurement.angular_velocity_noise_covariance

        variance = (cov1[0][0], cov1[1][1], cov1[2][2], cov2[0][0], cov2[1][1], cov2[2][2])

        noise = variance_6d(variance)

        edge = PriorBias(bias.instance, measurement, noise)

        new_vertices = create_new_vertices([bias])

        return GraphElement(edge, {bias.instance: t}, new_vertices)
