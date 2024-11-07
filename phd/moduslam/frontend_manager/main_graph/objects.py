from dataclasses import dataclass, field
from typing import Generic, TypeAlias, TypeVar

from phd.measurements.processed_measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex

V = TypeVar("V", bound=Vertex)

VertexWithTimestamp: TypeAlias = tuple[V, int]
VerticesTable: TypeAlias = dict[VertexCluster, list[VertexWithTimestamp[V]]]


@dataclass
class GraphElement(Generic[V]):
    edge: Edge
    new_vertices: VerticesTable[V] = field(default_factory=dict)


@dataclass
class GraphCandidate:
    graph: Graph
    elements: list[GraphElement]
    leftovers: list[Measurement]
