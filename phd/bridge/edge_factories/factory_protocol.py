from dataclasses import dataclass
from typing import Generic, Protocol, TypeVar

from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.utils.auxiliary_dataclasses import TimeRange

V = TypeVar("V", bound=Vertex)


@dataclass
class VertexWithStatus(Generic[V]):
    instance: V
    cluster: VertexCluster
    timestamp: int
    is_new: bool = False


class EdgeFactory(Protocol):
    @classmethod
    def create(
        cls,
        graph: Graph,
        clusters: dict[VertexCluster, TimeRange],
        measurement,
    ) -> GraphElement | list[GraphElement]:
        """Creates new element(s) for the graph based on the given measurement.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a measurement to create edge(s).
        """
