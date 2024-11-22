from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.utils import (
    create_vertex_i_with_status,
    get_cluster,
    get_new_items,
)
from phd.measurements.processed_measurements import ImuBias as BiasMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.imu_bias import ImuBias as PriorBias
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import ImuBias
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import zero_vector3


class Factory(EdgeFactory):
    _vertex_type = PoseVertex

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: BiasMeasurement
    ) -> GraphElement:
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

        cluster = get_cluster(clusters, t)
        zero_bias = (zero_vector3, zero_vector3)
        velocity = create_vertex_i_with_status(ImuBias, storage, cluster, t, zero_bias)

        edge = PriorBias(velocity.instance, measurement)

        new_vertices = get_new_items([velocity])

        return GraphElement(edge, new_vertices)
