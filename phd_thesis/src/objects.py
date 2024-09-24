from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Vertex:
    """An instance to accumulate the measurements belonging to the same timestamp."""

    measurements: tuple[int, ...]


@dataclass
class Edge:
    """An edges between 2 vertices.

    Consist from pre-integrated measurements only.
    """

    vertex1: Vertex
    vertex2: Vertex


@dataclass
class Graph:
    """A combination of vertices and edges to be evaluated and connected to the
    Graph."""

    vertices: list[Vertex]
    edges: list[Edge]
