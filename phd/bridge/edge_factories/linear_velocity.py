import gtsam

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.noise_models import covariance3x3_noise_model
from phd.bridge.edge_factories.utils import create_new_vertex
from phd.measurements.processed_measurements import (
    LinearVelocity as VelocityMeasurement,
)
from phd.moduslam.frontend_manager.main_graph.edges.custom import PriorVelocity
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import LinearVelocity


class Factory(EdgeFactory):
    _vertex_type = LinearVelocity

    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement: VelocityMeasurement
    ) -> GraphElement:
        """Creates a new edge with prior linear velocity factor.

        Args:
            graph: a main graph.

            cluster: a common cluster for new vertices.

            measurement: a linear velocity [Vx, Vy, Vz].

        Returns:
            a new element.
        """
        is_new_velocity = False
        velocity = cluster.get_latest_vertex(cls._vertex_type)

        if velocity:
            vertex = velocity
        else:
            is_new_velocity = True
            vertex = create_new_vertex(cls._vertex_type, graph)

        noise = covariance3x3_noise_model(measurement.noise_covariance)
        factor = gtsam.PriorFactorVector(vertex.backend_index, measurement.velocity, noise)
        edge = PriorVelocity(vertex, measurement, factor, noise)

        if is_new_velocity:
            new_vertices = {cluster: [(vertex, measurement.timestamp)]}
            element = GraphElement(edge, new_vertices)
        else:
            element = GraphElement(edge)

        return element
