import logging
from collections.abc import Iterable

import gtsam
from hydra.core.hydra_config import HydraConfig
from plum import dispatch, overload

from slam.frontend_manager.graph.edges.edge_storage import EdgeStorage
from slam.frontend_manager.graph.edges.edges import Edge, GraphEdge
from slam.frontend_manager.graph.vertices.vertex_storage import VertexStorage
from slam.frontend_manager.graph.vertices.vertices import GraphVertex, Vertex

logger = logging.getLogger(__name__)


class Graph:
    """
    High-level Graph.
    Includes gtsam.NonlinearFactorGraph.
    TODO: add logic to remove detached vertices from the graph.
    """

    def __init__(self) -> None:
        self.vertex_storage = VertexStorage[Vertex]()
        self.edge_storage = EdgeStorage[Edge]()
        self._factor_graph = gtsam.NonlinearFactorGraph()

    @overload
    def _delete_vertex(self, vertex: GraphVertex) -> None:
        """
        @overload.
        Deletes vertex from the graph.

        Args:
            vertex (GraphVertex): vertex to be deleted from the graph.
        """

    @overload
    def _delete_vertex(self, vertices: Iterable[GraphVertex]) -> None:
        """
        @overload.
        Deletes multiple vertices from the graph.

        Args:
            vertices (Iterable[GraphVertex]): vertices to be deleted from the graph.
        """
        for vertex in vertices:
            self._delete_vertex(vertex)

    @dispatch
    def _delete_vertex(self, vertex=None):
        """
        @overload.

        Calls:
            1. delete 1 vertex:
                Args:
                    vertex (GraphVertex): vertex to be deleted from the graph.

            2. delete multiple vertices:
                Args:
                    vertices (Iterable[GraphVertex]): vertices to be deleted from the graph.
        """

    @property
    def factor_graph(self) -> gtsam.NonlinearFactorGraph:
        """
        gtsam.NonlinearFactorGraph.
        Returns:
            (gtsam.NonlinearFactorGraph): non-linear factor graph.
        """
        return self._factor_graph

    @overload
    def set_prior(self) -> None:
        """
        @overload.
        Initialize the graph with prior vertices and edges.
        """
        raise NotImplementedError

    @overload
    def set_prior(self, config: HydraConfig) -> None:
        """
        @overload.
        Initialize the graph with prior vertices and edges from config.
        """
        raise NotImplementedError

    @dispatch
    def set_prior(self, config=None):
        """
        @overload.

        Calls:
            1. default: no args.

            2. with the config:
                Args:
                    config (HydraConfig): config with prior vertices and edges.

        """
        raise NotImplementedError

    @overload
    def add_edge(self, edge: GraphEdge) -> None:
        """
        @overload.
        Adds edge to the graph.

        Args:
            edge (GraphEdge): new edge to be added to the graph.
        """
        self.vertex_storage.add(edge.vertices)
        self.edge_storage.add(edge)
        self._factor_graph.add(edge.gtsam_factor)

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
            1. add single edge:
                Args:
                    edge (GraphEdge): new edge to be added to the graph.

            2. add multiple edges:
                Args:
                    edges (Iterable[GraphEdge]): new edges to be added to the graph.
        """

    @overload
    def delete_edge(self, edge: GraphEdge) -> None:
        """
        @overload.
        Deletes edge from the graph.

        Args:
            edge: edge to be deleted from the graph.
        """

    @overload
    def delete_edge(self, edges: Iterable[GraphEdge]) -> None:
        """
        @overload.
        Deletes multiple edges from the graph.

        Args:
            edges (Iterable[GraphEdge]): edges to be deleted from the graph.
        """
        for edge in edges:
            self.delete_edge(edge)

    @dispatch
    def delete_edge(self, edge=None):
        """
        @overload.

        Calls:
            1. delete single edge:
                Args:
                    edge (GraphEdge): edge to be deleted from the graph.

            2. delete multiple edges:
                Args:
                    edges (Iterable[GraphEdge]): edges to be deleted from the graph.
        """

    def marginalize(self, edges: Iterable[GraphEdge]) -> None:
        """
        Marginalizes out edges.

        Args:
            edges (Iterable[GraphEdge]): edges to be marginalized out.
        """
