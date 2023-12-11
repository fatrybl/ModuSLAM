import logging
from collections import deque
from typing import Type

import gtsam
from hydra.core.hydra_config import HydraConfig
from plum import dispatch

from slam.frontend_manager.graph.edges import Edge
from slam.frontend_manager.graph.vertices import Vertex

logger = logging.getLogger(__name__)


class Graph:
    """
    High-level Graph. 
    Includes GTSAM Factor Graph.
    """

    def __init__(self) -> None:
        self.factor_graph = gtsam.NonlinearFactorGraph()
        self.vertices: set[Type[Vertex]] = set()
        self.edges: set[type[Edge]] = set()
        self.vertices_table: dict[str, deque[type[Vertex]]] = dict()

    @dispatch
    def set_prior(self, vertices: set[Vertex], edges: set[Edge]) -> None:
        """
        Initialize the graph with prior vertices and edges.
        """
        pass

    @dispatch
    def set_prior(self, config: HydraConfig) -> None:
        """
        Initialize the graph with prior vertices and edges from config.
        """
        pass

    def add_vertex(self, vertex: Vertex):
        """
        Adds a new vertex to the main graph and factor graph.

        Args:
            vertex (Vertex): vertex to be added.
        """
        # self.factor_graph.addPriorPose2(0, pose1, prior_noise)
        pass

    def add_edge(self, edge: Type[Edge]) -> None:
        """
        Adds a new vertex to the main graph and factor graph.

        Args:
            edge(Edge): edge to be added.
        """
        self.edges.add(edge)
        self.factor_graph.add(edge.gtsam_factor)

    def delete_vertex(self, vertex_id: int) -> None:
        """
        Deletes vertex and all connected edges from the main graph and factor graph based on id.

        Args:
            vertex_id (int): vertex id 
        """
        pass

    def delete_edge(self, edge_id: int) -> None:
        """
        Deletes vertex and all connected edges from the main graph and factor graph based on id.

        Args:
            vertex_id (int): vertex id 
        """
        pass

    def update_graph(self, factor_graph: gtsam.NonlinearFactorGraph) -> None:
        """
        Updates factor graph

        Args:
            factor_graph (gtsam.NonlinearFactorGraph): new factor graph.
        """
        # self.factor_graph = factor_graph
        pass
