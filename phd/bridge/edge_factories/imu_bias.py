from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.measurements.processed_measurements import Pose as PoseMeasurement
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
        """Creates a new edge with prior IMU bias factor.

        Args:
            graph: a main graph.

            cluster: a common cluster for new vertices.

            measurement: an angular velocity and linear acceleration initial biases.

        Returns:
            a new element.
        """
        raise NotImplementedError
