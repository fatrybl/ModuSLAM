import logging

import gtsam

from moduslam.logger.logging_config import frontend_manager
from phd.moduslam.frontend_manager.main_graph.edge_storage.storage import EdgeStorage
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.element import GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex

logger = logging.getLogger(frontend_manager)


class Graph:
    """High-level Graph.

    Includes gtsam.NonlinearFactorGraph.
    """

    def __init__(self) -> None:
        self._factor_graph = gtsam.NonlinearFactorGraph()
        self._vertex_storage = VertexStorage()
        self._edge_storage = EdgeStorage()
        self._connections: dict[Vertex, set[Edge]] = {}

    @property
    def factor_graph(self) -> gtsam.NonlinearFactorGraph:
        """Backend Factor Graph."""
        return self._factor_graph

    @property
    def vertex_storage(self) -> VertexStorage:
        """Storage for the vertices of the graph."""
        return self._vertex_storage

    @property
    def edge_storage(self) -> EdgeStorage:
        """Storage for the edges of the graph."""
        return self._edge_storage

    @property
    def connections(self) -> dict[Vertex, set[Edge]]:
        """Connections of vertices with edges."""
        return self._connections

    def get_connected_edges(self, vertex: Vertex) -> set[Edge]:
        """Gets all edges connected to the vertex.

        Args:
            vertex: a target vertex.

        Returns:
            edges.
        """
        return self._connections[vertex]

    def add_element(self, element: GraphElement) -> None:
        """Adds new element to the graph.

        Args:
            element: a new element to add.
        """
        edge = element.edge
        edge.index = self._generate_index()
        self.edge_storage.add(edge)
        self.factor_graph.add(edge.factor)

        for cluster, vertices_with_timestamps in element.new_vertices.items():
            for vertex, timestamp in vertices_with_timestamps:
                self._vertex_storage.add(cluster, vertex, timestamp)
                self._add_connection(vertex, edge)

    def remove_edge(self, edge: Edge) -> None:
        """Removes an edge from the graph.

        Args:
            edge: an edge to be removed.
        """

        self._factor_graph.remove(edge.index)
        self._edge_storage.remove(edge)

        for vertex in edge.vertices:
            self._remove_connection(vertex, edge)

            if not self._connections[vertex]:
                self._vertex_storage.remove(vertex)

    def replace_edge(self, edge: Edge, element: GraphElement) -> None:
        """Replaces an existing edge with a new element.

        Args:
            edge: an edge to be replaced.

            element: a new element to replace the old edge.
        """
        self.remove_edge(edge)
        self.add_element(element)

    def remove_vertex(self, vertex: Vertex) -> None:
        """Removes vertex from the graph.

        Args:
            vertex: vertex to be deleted from the graph.
        """
        edges = self._connections[vertex]
        for edge in edges:
            self.remove_edge(edge)

    def update_vertices(self, values: gtsam.Values) -> None:
        """Updates the graph vertices with the new values.

        Args:
            values: GTSAM values.

        TODO: add update for non-optimizable vertices.
        """
        for vertex in self._vertex_storage.optimizable_vertices:
            vertex.update(values)

    def _generate_index(self) -> int:
        """Gets a unique index for the new edge based on the size of the factor graph.
        Gtsam Factor Graph sets a unique index to every factor being added to it. This
        guarantees the uniqueness of the index. However, the size of the factor graph is
        not equal to the number of factors in the graph, because the factor graph may
        contain empty slots (null ptr objects). When the factor is removed, the size of
        the factor graph does not change but a Null ptr is added to the corresponding
        factor.

        *P.S.
            To reduce the size of the factor graph, use the resize() method.

        Returns:
            unique index.
        """
        return self.factor_graph.size()

    def _add_connection(self, vertex: Vertex, edge: Edge) -> None:
        """Adds edge to the connection with the vertex.
        Args:
            vertex: vertex to which the edge is added.

            edge: edge to be added to the vertex.
        """
        if vertex not in self._connections:
            self._connections[vertex] = {edge}
        else:
            self._connections[vertex].add(edge)

    def _remove_connection(self, vertex: Vertex, edge: Edge) -> None:
        """Removes the connection between a vertex and an edge.

        Args:
            vertex: a vertex to remove the connection for.

            edge: an edge to remove the connection for.
        """
        self._connections[vertex].remove(edge)
