import logging
from collections.abc import Iterable

import gtsam

from src.logger.logging_config import frontend_manager
from src.measurement_storage.measurements.base import Measurement
from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.new_element import GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.utils.exceptions import (
    ItemExistsError,
    ItemNotExistsError,
    NotSubsetError,
    ValidationError,
)
from src.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class Graph:
    """High-level Graph with gtsam.NonlinearFactorGraph."""

    def __init__(self) -> None:
        self._factor_graph = gtsam.NonlinearFactorGraph()
        self._vertex_storage = VertexStorage()
        self._edges = OrderedSet[Edge]()
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
    def edges(self) -> OrderedSet[Edge]:
        """Storage for the edges of the graph."""
        return self._edges

    @property
    def connections(self) -> dict[Vertex, set[Edge]]:
        """Connections of vertices with edges."""
        return self._connections

    def get_backend_instances(self) -> gtsam.Values:
        """Gets backend instances for optimizable vertices.

        Returns:
            GTSAM backend instances.
        """
        values = gtsam.Values()

        for vertex in self._vertex_storage.optimizable_vertices:
            values.insert(vertex.backend_index, vertex.backend_instance)

        return values

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

        Raises:
            ValidationError: if the validation of an element fails.
        """
        edge = element.edge

        try:
            self._validate_graph_element(element)
        except (ItemExistsError, ItemNotExistsError) as e:
            msg = f"Validation failed: {e}"
            logger.error(msg)
            raise ValidationError(msg)

        edge.index = self._generate_index()
        self.edges.add(edge)
        self.factor_graph.add(edge.factor)

        for new_vertex in element.new_vertices:
            self._vertex_storage.add(new_vertex)

        for vertex in edge.vertices:
            self._add_connection(vertex, edge)

    def add_elements(self, elements: Iterable[GraphElement]):
        """Adds multiple elements.

        Args:
            elements: multiple elements to add.
        """
        for element in elements:
            self.add_element(element)

    def remove_edge(self, edge: Edge) -> None:
        """Removes an edge from the graph.

        Args:
            edge: an edge to be removed.
        """

        try:
            self._validate_removing_edge(edge)

        except ItemNotExistsError as e:
            msg = f"Validation failed: {e}"
            logger.error(msg)
            raise ValidationError(msg)

        self._factor_graph.remove(edge.index)
        self._edges.remove(edge)

        for vertex in edge.vertices:
            self._connections[vertex].remove(edge)

            if not self._connections[vertex]:
                self._vertex_storage.remove(vertex)
                del self._connections[vertex]

    def replace_edge(self, edge: Edge, new_edge: Edge) -> None:
        """Replaces an existing edge with a new one of the same type.

        Args:
            edge: an edge to be replaced.

            new_edge: a new edge.

        Raises:
            ValidationError: if the validation fails.
        """
        try:
            self._validate_replace_edge(edge, new_edge)
        except (ItemNotExistsError, ItemExistsError, TypeError, NotSubsetError) as e:
            msg = f"Validation failed: {e}"
            logger.error(msg)
            raise ValidationError(msg)

        new_edge.index = edge.index
        self._edges.remove(edge)
        self._edges.add(new_edge)
        self._factor_graph.replace(edge.index, new_edge.factor)

        for vertex in edge.vertices:
            self._connections[vertex].remove(edge)
            self._connections[vertex].add(new_edge)

    def remove_vertex(self, vertex: Vertex) -> None:
        """Removes vertex from the graph.

        Args:
            vertex: vertex to be deleted from the graph.

        Raises:
            ValidationError: if the vertex is not present in the graph.
        """
        if vertex not in self._vertex_storage:
            raise ValidationError(f"Vertex {vertex} is not present in the graph.")

        edges = self._connections[vertex]
        for edge in edges.copy():  # copy to avoid set changes during iterations.
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

    def _validate_graph_element(self, element: GraphElement) -> None:
        """Validates a new graph element before adding.

        Args:
            element: a graph element to validate.

        Raises:
            ItemExistsError:
                1. if an edge already exists.
                2. if a vertex from new vertices already exists in the graph.
                3. if a vertex of the edge exists in the graph and in new vertices.
                4. if a GTSAM factor exists in the GTSAM factor graph.

            ItemNotExistsError:
                1. if a vertex of the edge does not exist in the graph and in new vertices.
        """
        edge = element.edge
        new_vertices_set = {v.instance for v in element.new_vertices}

        if edge in self._edges:
            raise ItemExistsError(f"Edge {edge} already exists.")

        if edge.index and self._factor_graph.exists(edge.index):
            raise ItemExistsError(f"Factor {edge.factor} already exists in the factor graph.")

        for vertex in new_vertices_set:
            if vertex in self._vertex_storage:
                raise ItemExistsError(f"Vertex {vertex} already exists in the graph.")

        for vertex in edge.vertices:
            if vertex in self._vertex_storage and vertex in new_vertices_set:
                raise ItemExistsError(
                    f"Vertex {vertex} is already present in the graph and cannot be added."
                )

            if vertex not in self._vertex_storage and vertex not in new_vertices_set:
                raise ItemNotExistsError(
                    f"Vertex {vertex} is neither present in the graph nor in the new vertices."
                )

    def _validate_removing_edge(self, edge: Edge) -> None:
        """Validates an edge before removing from the graph.

        Args:
            edge: edge to be removed.

        Raises:
            ItemNotExistsError: if the edge does not exist.
        """
        if edge not in self._edges:
            raise ItemNotExistsError(f"Edge {edge} does not exist.")

        if not self._factor_graph.exists(edge.index):
            raise ItemNotExistsError(f"No edge with index{edge.index} in GTSAM factor graph.")

    def _validate_replace_edge(self, edge: Edge, new_edge: Edge):
        """Validates an edge with a new element before replacing.

        Args:
            edge: an edge to be replaced.

            new_edge: a new edge.

        Raises:
            ItemNotExistsError: if the edge to be replaced does not exist.

            ItemExistsError: if a new edge already exists.

            TypeError: if the types of the existing edge and the new edge do not match.
        """
        if edge not in self._edges:
            raise ItemNotExistsError(f"Edge {edge} does not exist.")

        if new_edge in self._edges:
            raise ItemExistsError(f"Edge {new_edge} already exists.")

        if type(edge) is not type(new_edge):
            raise TypeError("Type mismatch between the existing edge and the new edge.")

        if edge.vertices != new_edge.vertices:
            raise NotSubsetError("Vertices of the new edge do not match with the existing edge.")

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


class GraphCandidate:
    def __init__(
        self, graph: Graph, elements: list[GraphElement], leftovers: list[Measurement] | None = None
    ):
        self.graph = graph
        self.elements = elements
        self.leftovers = leftovers
