from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Factory(EdgeFactory):
    _vertex_type = PoseVertex

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: PoseMeasurement
    ) -> GraphElement:
        """Creates a new edge with prior IMU bias factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: an angular velocity and linear acceleration initial biases.

        Returns:
            a new element.
        """
        raise NotImplementedError
