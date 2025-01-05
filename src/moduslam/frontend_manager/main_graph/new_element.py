from dataclasses import dataclass, field
from typing import Generic, TypeVar

from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.utils.exceptions import ItemExistsError, ValidationError

E = TypeVar("E", bound=Edge)
V = TypeVar("V", bound=Vertex)


@dataclass
class NewVertex(Generic[V]):
    instance: V
    cluster: VertexCluster
    timestamp: int

    def __post_init__(self):
        if self.instance in self.cluster:
            raise ItemExistsError(f"Vertex{self.instance} already exists in cluster")


@dataclass
class GraphElement(Generic[E]):
    """New graph element.

    Raises:
        ValidationError: if a vertex is new but not in the edge.
    """

    edge: E
    new_vertices: list[NewVertex] = field(default_factory=list)

    def __post_init__(self):
        new_vertices = {v.instance for v in self.new_vertices}
        edge_vertices = set(self.edge.vertices)

        if not new_vertices.issubset(edge_vertices):
            raise ValidationError(
                f"Validation failed: some vertices in new_vertices are not in edge.vertices. "
                f"Missing: {new_vertices - edge_vertices}"
            )

        timestamp_cluster_map: dict[int, VertexCluster] = {}
        for new_vertex in self.new_vertices:
            if new_vertex.timestamp in timestamp_cluster_map:
                existing_cluster = timestamp_cluster_map[new_vertex.timestamp]
                if existing_cluster != new_vertex.cluster:
                    raise ValidationError(
                        f"Validation failed: different clusters found {existing_cluster, new_vertex.cluster} "
                        f"for timestamp{new_vertex.timestamp}"
                    )
            else:
                timestamp_cluster_map[new_vertex.timestamp] = new_vertex.cluster

        del timestamp_cluster_map
