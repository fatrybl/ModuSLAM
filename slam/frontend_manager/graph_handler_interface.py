from collections.abc import Iterable
from dataclasses import dataclass

from slam.frontend_manager.graph.base_vertices import Vertex
from slam.frontend_manager.graph.graph import Graph


@dataclass
class Request:
    """Request for vertex."""

    vertex_type: type[Vertex]
    vertex_id: int | None = None
    vertex_timestamp: int | None = None
    last: bool = False
    first: bool = False

    def __post_init__(self):
        if (
            self.vertex_timestamp is not None
            and self.vertex_id is not None
            and self.last
            and self.first
        ):
            raise ValueError(
                "vertex_timestamp, vertex_id, last, first cannot be set simultaneously"
            )


class GraphHandlerInterface:
    """Interface for handlers that need to interact with the graph."""

    _graph: Graph | None = None

    @classmethod
    def set_graph(cls, graph: Graph):
        cls._graph = graph

    @classmethod
    def get_graph(cls) -> Graph:
        if cls._graph is None:
            raise ValueError("Graph is not initialized")
        else:
            return cls._graph

    @classmethod
    def get_vertex(cls, request: Request) -> Vertex:
        v_type = request.vertex_type
        graph = cls.get_graph()
        vertices = graph.vertex_storage.get_vertices(v_type)
        return vertices[0]

    @classmethod
    def get_vertices(cls, requests: Iterable[Request]) -> list[Vertex]:
        return [cls.get_vertex(request) for request in requests]
