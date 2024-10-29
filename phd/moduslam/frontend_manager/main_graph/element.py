from dataclasses import dataclass, field
from typing import TypeAlias

from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex

VertexWithTimestamp: TypeAlias = tuple[Vertex, int]


@dataclass
class GraphElement:
    edge: Edge
    new_vertices: dict[VertexCluster, list[VertexWithTimestamp]] = field(default_factory=dict)
