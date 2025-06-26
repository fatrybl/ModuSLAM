from dataclasses import dataclass, field
from typing import Generic, TypeVar

from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.utils.exceptions import ItemExistsError, NotSubsetError, ValidationError

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
    vertex_timestamp_table: dict[Vertex, int]
    new_vertices: tuple[NewVertex, ...] = field(default_factory=lambda: ())

    def __post_init__(self):
        try:
            self._validate_new_vertices()
            self._validate_clusters()
            self._validate_table_vertices()
            self._validate_table_timestamps()
        except (NotSubsetError, ValueError) as e:
            raise ValidationError(e)

    def _validate_new_vertices(self) -> None:
        """Validates that all new vertices are in the edge.

        Raises:
            NotSubsetError: if some vertices in new_vertices are not in edge.vertices.
        """
        new_vertices = {v.instance for v in self.new_vertices}
        edge_vertices = set(self.edge.vertices)

        if not new_vertices.issubset(edge_vertices):
            raise NotSubsetError(
                f"Some vertices in new_vertices are not in edge.vertices. "
                f"Missing: {new_vertices - edge_vertices}"
            )

    def _validate_clusters(self) -> None:
        """Validates that all new vertices have the same cluster for the same timestamp.

        Raises:
            ValueError: if multiple clusters found for the same timestamp.
        """
        time_cluster_map: dict[int, VertexCluster] = {}
        for vertex in self.new_vertices:
            if vertex.timestamp in time_cluster_map:
                existing_cluster = time_cluster_map[vertex.timestamp]
                if existing_cluster != vertex.cluster:
                    raise ValueError(
                        f"Multiple clusters found: {existing_cluster, vertex.cluster} "
                        f"for timestamp{vertex.timestamp}"
                    )
            else:
                time_cluster_map[vertex.timestamp] = vertex.cluster

    def _validate_table_timestamps(self) -> None:
        """Validates that all vertices in vertex_timestamp_table have non-negative
        timestamps.

        Raises:
            ValueError: if some timestamps are negative.
        """
        for timestamp in self.vertex_timestamp_table.values():
            if timestamp < 0:
                raise ValueError("Timestamp should be positive")

    def _validate_table_vertices(self) -> None:
        """Validates that vertices in the vertex_timestamp_table are present in edge
        vertices.

        Raises:
            NotSubsetError: missmatch between edge`s vertices and vertex_timestamp_table.
        """
        edge_vertices_set = set(self.edge.vertices)
        table_vertices_set = set(self.vertex_timestamp_table.keys())

        if table_vertices_set != edge_vertices_set:
            raise NotSubsetError(
                f"Missmatch between edge`s vertices and vertices in vertex_timestamp_table. "
                f"Missing: {edge_vertices_set - table_vertices_set}"
            )
