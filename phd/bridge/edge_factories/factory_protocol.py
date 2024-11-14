from typing import Protocol

from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)


class EdgeFactory(Protocol):
    @classmethod
    def create(
        cls, graph: Graph, cluster: VertexCluster, measurement
    ) -> GraphElement | list[GraphElement]:
        """Creates new element(s) for the graph based on the given measurement.

        Args:
            graph: a main graph.

            cluster: a common cluster for new vertices.

            measurement: a measurement to create edge(s).
        """
