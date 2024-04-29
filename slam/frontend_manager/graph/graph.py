import logging
from collections.abc import Iterable
from typing import Generic, overload

import gtsam
from plum import dispatch

from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.base_vertices import GraphVertex, OptimizableVertex
from slam.frontend_manager.graph.edge_storage import EdgeStorage
from slam.frontend_manager.graph.vertex_storage import VertexStorage

logger = logging.getLogger(__name__)


class Graph(Generic[GraphVertex, GraphEdge]):
    """High-level Graph.

    Includes gtsam.NonlinearFactorGraph.
    TODO:
        1) implement edges deletion with factors modification.
        2) implement marginalization of vertices.
    """

    def __init__(self) -> None:
        self.vertex_storage = VertexStorage[GraphVertex]()
        self.edge_storage = EdgeStorage[GraphEdge]()
        self.factor_graph = gtsam.NonlinearFactorGraph()

    @property
    def gtsam_values(self) -> gtsam.Values:
        """GTSAM values of the graph.

        TODO: add tests.
        """
        vertices = self.vertex_storage.optimizable_vertices
        values = gtsam.Values()
        unique_vertices: dict[int, OptimizableVertex] = {}

        for vertex in vertices:
            if vertex.gtsam_index not in unique_vertices:
                unique_vertices[vertex.gtsam_index] = vertex

        [
            values.insert(vertex.gtsam_index, vertex.gtsam_instance)
            for vertex in unique_vertices.values()
        ]

        return values

    @overload
    def add_edge(self, edge: GraphEdge) -> None:
        """
        @overload.

        Adds edge to the graph.

        Args:
            edge (GraphEdge): new edge to be added to the graph.
        """
        edge.index = self._set_index()

        vertices = sorted(edge.all_vertices, key=lambda v: v.timestamp)
        [vertex.edges.add(edge) for vertex in vertices]

        self.vertex_storage.add(vertices)
        self.edge_storage.add(edge)
        self.factor_graph.add(edge.factor)

    @overload
    def add_edge(self, edges: Iterable[GraphEdge]) -> None:
        """
        @overload.

        Adds multiple edges to the graph.

        Args:
            edges (Iterable[GraphEdge]): new edges to be added to the graph.
        """

        for edge in edges:
            self.add_edge(edge)

    @dispatch
    def add_edge(self, edge=None):
        """
        @overload.

        Calls:
            1.  Adds edge to the graph:

                Args:
                    edge (GraphEdge): new edge to be added to the graph.

            2.  Adds multiple edges to the graph:

                Args:
                    edges (Iterable[GraphEdge]): new edges to be added to the graph.
        """

    @overload
    def remove_edge(self, edge: GraphEdge) -> None:
        """
        @overload.

        Removes edge from the graph.

        Args:
            edge (GraphEdge): edge to be deleted from the graph.
        """

        self.factor_graph.remove(edge.index)
        self.edge_storage.remove(edge)
        for vertex in edge.all_vertices:
            vertex.edges.remove(edge)
            if not vertex.edges:
                self.vertex_storage.remove(vertex)

    @overload
    def remove_edge(self, edges: Iterable[GraphEdge]) -> None:
        """
        @overload.

        Removes multiple edges from the graph.

        Args:
            edges (Iterable[GraphEdge]): edges to be deleted from the graph.
        """
        while edges:
            edge = next(iter(edges))
            self.remove_edge(edge)

    @dispatch
    def remove_edge(self, edge=None):
        """
        @overload.

        TODO: add tests.

        Calls:
            1.  Removes single edge:

                Args:
                    edge (GraphEdge): edge to be deleted from the graph.

            2.  Removes multiple edges:

                Args:
                    edges (Iterable[GraphEdge]): edges to be deleted from the graph.
        """

    @overload
    def remove_vertex(self, vertex: GraphVertex) -> None:
        """
        @overload.

        Removes vertex from the graph.

        Args:
            vertex (GraphVertex): vertex to be deleted from the graph.
        """
        self.remove_edge(vertex.edges)

    @overload
    def remove_vertex(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.

        Removes multiple vertices from the graph.

        Args:
            vertices (Iterable[GraphVertex]): vertices to be deleted from the graph.
        """
        while vertices:
            vertex = next(iter(vertices))
            self.remove_vertex(vertex)

    @dispatch
    def remove_vertex(self, vertex=None):
        """
        @overload.

        TODO: add tests.

        Calls:
            1.  Removes 1 vertex:

                Args:
                    vertex (GraphVertex): vertex to be deleted from the graph.

            2.  Removes multiple vertices:

                Args:
                    vertices (Iterable[GraphVertex]): vertices to be deleted from the graph.
        """

    def update(self, values: gtsam.Values) -> None:
        """Updates the graph with new values.

        Args:
            values: GTSAM values.
        """

        self.vertex_storage.update_optimizable_vertices(values)
        self.vertex_storage.update_non_optimizable_vertices()

    def marginalize(self, vertices: Iterable[GraphVertex]) -> None:
        """Marginalizes out vertices.

        Not implemented.
        """
        raise NotImplementedError

    def _set_index(self) -> int:
        """Sets unique index for the new edge base on the size of the factor graph.
        Gtsam factor graph sets index to the factor by exploiting the size of the factor
        graph. This guarantees the uniqueness of the index. However, the size of the
        factor graph is not equal to the number of factors in the graph, because the
        factor graph may contain empty slots (null ptr objects). When the factor is
        removed, the size of the factor graph does not change. To reduce the size of the
        factor graph, the resize() method should be called.

        Returns:
            unique index.
        """
        return self.factor_graph.size()
