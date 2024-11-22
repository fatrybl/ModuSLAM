from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.utils import (
    create_vertex_i_with_status,
    get_cluster,
    get_new_items,
)
from phd.measurements.processed_measurements import (
    LinearVelocity as VelocityMeasurement,
)
from phd.moduslam.frontend_manager.main_graph.edges.linear_velocity import (
    LinearVelocity as PriorVelocity,
)
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    covariance3x3_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import LinearVelocity
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import zero_vector3


class Factory(EdgeFactory):
    _vertex_type = LinearVelocity

    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement: VelocityMeasurement,
    ) -> GraphElement:
        """Creates a new edge with prior linear velocity factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a linear velocity [Vx, Vy, Vz].

        Returns:
            a new element.
        """
        t = measurement.timestamp
        storage = graph.vertex_storage

        cluster = get_cluster(clusters, t)
        velocity = create_vertex_i_with_status(LinearVelocity, storage, cluster, t, zero_vector3)

        noise_model = covariance3x3_noise_model(measurement.noise_covariance)
        edge = PriorVelocity(velocity.instance, measurement, noise_model)

        new_vertices = get_new_items([velocity])

        return GraphElement(edge, new_vertices)
