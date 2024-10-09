import logging
from collections.abc import Iterable
from typing import Generic

import gtsam

from moduslam.frontend_manager.graph.base_edges import BaseEdge
from moduslam.frontend_manager.graph.base_vertices import BaseVertex, OptimizableVertex
from moduslam.frontend_manager.graph.edge_storage import EdgeStorage
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.logger.logging_config import frontend_manager

logger = logging.getLogger(frontend_manager)


class Graph(Generic[BaseVertex, BaseEdge]):
    """High-level Graph.

    Includes gtsam.NonlinearFactorGraph.
    """

    def __init__(self) -> None:
        self._factor_graph = gtsam.NonlinearFactorGraph()
        self._vertex_storage = VertexStorage[BaseVertex]()
        self._edge_storage = EdgeStorage[BaseEdge]()
        self._connections: dict[BaseVertex, set[BaseEdge]] = {}

    @property
    def factor_graph(self) -> gtsam.NonlinearFactorGraph:
        """Backend Factor Graph."""
        return self._factor_graph

    @property
    def vertex_storage(self) -> VertexStorage[BaseVertex]:
        """Storage for the vertices of the graph."""
        return self._vertex_storage

    @property
    def edge_storage(self) -> EdgeStorage[BaseEdge]:
        """Storage for the edges of the graph."""
        return self._edge_storage

    @property
    def backend_values(self) -> gtsam.Values:
        """Internal values of the factor graph."""
        values = gtsam.Values()
        unique_vertices = self._get_unique_optimizable_vertices()
        for vertex in unique_vertices.values():
            values.insert(vertex.backend_index, vertex.backend_instance)
        return values

    @property
    def connections(self) -> dict[BaseVertex, set[BaseEdge]]:
        """Connections of vertices with edges."""
        return self._connections

    def get_connected_edges(self, vertex: BaseVertex) -> set[BaseEdge]:
        """Gets edges connected to the vertex.

        Args:
            vertex: vertex for which the edges are retrieved.

        Returns:
            set of edges connected to the vertex.
        """
        return self._connections.get(vertex, set())

    def add_edge(self, edge: BaseEdge) -> None:
        """Adds edge to the graph.

        Args:
            edge: new edge to be added to the graph.

        TODO: timestamped based sorting has been removed. Check if it works.
        TODO: add tests for the existing edges being added.
        TODO: add more efficient way to update the connections for the existing edges. Now it takes O(N) time.
        """
        if edge in self._edge_storage.edges:
            self._update_edge_connections(edge)
            return

        edge.index = self._set_index()

        self._edge_storage.add(edge)
        self._vertex_storage.add(edge.vertices)
        self.factor_graph.add(edge.factor)

        for v in edge.vertices:
            self._add_connection(v, edge)

    def add_edges(self, edges: Iterable[BaseEdge]) -> None:
        """Adds multiple edges to the graph.

        Args:
            edges: new edges to be added to the graph.
        """
        for edge in edges:
            self.add_edge(edge)

    def remove_edge(self, edge: BaseEdge) -> None:
        """Removes edge from the graph.

        Args:
            edge: edge to be deleted from the graph.
        """

        self.factor_graph.remove(edge.index)
        self._edge_storage.remove(edge)
        for vertex in edge.vertices:
            self._remove_connection(vertex, edge)

    def remove_edges(self, edges: Iterable[BaseEdge]) -> None:
        """Removes multiple edges from the graph.

        Args:
            edges: edges to be deleted from the graph.
        """
        edges_copy = list(edges)  # to avoid changing the size of collection during iterations.
        for edge in edges_copy:
            self.remove_edge(edge)

    def remove_vertex(self, vertex: BaseVertex) -> None:
        """Removes vertex from the graph.

        Args:
            vertex: vertex to be deleted from the graph.
        """
        edges = self._connections.get(vertex, None)
        self.remove_edges(edges) if edges else None
        self._vertex_storage.remove(vertex)
        self._connections.pop(vertex, None)

    def remove_vertices(self, vertices: Iterable[BaseVertex]) -> None:
        """Removes multiple vertices from the graph.

        Args:
            vertices: vertices to be deleted from the graph.
        """
        for vertex in vertices:
            self.remove_vertex(vertex)

    def update_connections(
        self, original_vertices: set[BaseVertex], modified_edge: BaseEdge
    ) -> None:
        """Updates edge`s connections in the graph. Does not update backend factor
        graph.

        Args:
            original_vertices: vertices of an edge before modifications.

            modified_edge: edge with modified vertices.
        """
        modified_vertices = set(modified_edge.vertices)

        for vertex in original_vertices:
            if vertex not in modified_vertices:
                self._remove_connection(vertex, modified_edge)

        for vertex in modified_vertices:
            if vertex not in original_vertices:
                self._add_connection(vertex, modified_edge)
            if vertex not in self._vertex_storage.vertices:
                self._vertex_storage.add(vertex)

    def update(self, values: gtsam.Values) -> None:
        """Updates the graph with new values.

        Args:
            values: GTSAM values.

        TODO: add update for non-optimizable vertices.
        """

        self._vertex_storage.update_optimizable_vertices(values)

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

    def _get_unique_optimizable_vertices(self) -> dict[int, OptimizableVertex]:
        """Gets vertices with unique backend indices.

        Returns:
            dict of indices and vertices.
        """
        unique_vertices: dict[int, OptimizableVertex] = {}

        for vertex in self._vertex_storage.optimizable_vertices:
            if vertex.backend_index not in unique_vertices:
                unique_vertices[vertex.backend_index] = vertex

        return unique_vertices

    def _add_connection(self, vertex: BaseVertex, edge: BaseEdge) -> None:
        """Adds edge to the connection with the vertex.
        Args:
            vertex: vertex to which the edge is added.

            edge: edge to be added to the vertex.
        """
        if vertex not in self._connections:
            self._connections[vertex] = {edge}
        else:
            self._connections[vertex].add(edge)

    def _update_edge_connections(self, edge: BaseEdge) -> None:
        """Updates connections of the edge with the vertices.

        Args:
            edge: edge to be updated.
        """
        new_vertices = set(edge.vertices)

        for vertex, edges in self._connections.items():
            if edge in edges:
                self._connections[vertex].remove(edge)

        for vertex in new_vertices:
            self._add_connection(vertex, edge)
            if vertex not in self._vertex_storage.vertices:
                self._vertex_storage.add(vertex)

    def _remove_connection(self, vertex: BaseVertex, edge: BaseEdge) -> None:
        """Removes edge from the connection with the vertex.

        Args:
            vertex: vertex from which the edge is removed.

            edge: edge to be removed from the vertex.

        Attention:
           if all edges are removed from connection, the vertex still exists in the connection.
        """

        if vertex in self._connections and edge in self._connections[vertex]:
            self._connections[vertex].remove(edge)
