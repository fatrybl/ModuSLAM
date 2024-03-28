import logging
from typing import Generic

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.index_generator import IndexStorage, generate_index
from slam.frontend_manager.graph.vertices import GraphVertex
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.tables_initializer import init_handler_edge_factory_table
from slam.system_configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class GraphMerger(Generic[GraphVertex, GraphEdge]):
    """Merges the graph candidate with the main graph."""

    def __init__(self, config: GraphMergerConfig) -> None:
        self._table: dict[Handler, EdgeFactory] = init_handler_edge_factory_table(
            config.handler_edge_factory_table
        )

    @property
    def handler_edge_factory_table(self) -> dict[Handler, EdgeFactory]:
        """A table to represent the connections between handlers & edge factories.

        Returns:
            (dict[Handler, EdgeFactory]): handler -> edge factory table.
        """
        return self._table

    @staticmethod
    def _create_vertex(
        index_storage: IndexStorage, vertex_type: type[GraphVertex], timestamp: int
    ) -> GraphVertex:
        """
        Creates a vertex instance for the given edge factory.
        Generates a unique index of the vertex for the given graph.
        Args:
            index_storage (IndexStorage): storage of unique indices.
            vertex_type (type[GraphVertex]): types of the vertices.
            timestamp (int): timestamp of the vertex.

        Returns:
            (GraphVertex): new vertex instance.
        """
        vertex = vertex_type()
        vertex.index = generate_index(index_storage)
        vertex.timestamp = timestamp
        return vertex

    def _create_vertex_table(
        self, graph: Graph, state: State
    ) -> dict[EdgeFactory, list[GraphVertex]]:
        """
        Creates vertex instances for the state.
        The instances are empty: not initialized yet.

        Args:
            state (State): state with measurements.

        Returns:
            (dict[EdgeFactory, GraphVertex]): "Edge Factory -> Graph Vertex(s)" table.

        """

        table: dict[EdgeFactory, list[GraphVertex]] = {}
        indices = graph.vertex_storage.index_storage
        timestamp = state.timestamp
        edge_factories = self._table.values()

        vertices_types = set[type[GraphVertex]]()
        type_instance_table = dict[type[GraphVertex], GraphVertex]()
        vertices_types = vertices_types.union(
            *(factory.vertices_types for factory in edge_factories)
        )

        type_instance_table = {
            v_type: self._create_vertex(indices, v_type, timestamp) for v_type in vertices_types
        }

        for factory in edge_factories:
            vertices = [type_instance_table[v_type] for v_type in factory.vertices_types]
            table[factory] = vertices

        return table

    def _create_edges(
        self,
        graph: Graph,
        factory_vertices_table: dict[EdgeFactory, list[GraphVertex]],
        handler: Handler,
        measurements: OrderedSet[Measurement],
    ) -> list[GraphEdge]:
        """
        Creates edges for the state.
        Note:
            Each handler is being processed by the corresponding edge factory.
            Every edge factory uses vertex of the given state.

        Args:
            graph (Graph): main graph.
            factory_vertices_table (dict[EdgeFactory, list[GraphVertex]]): "edge factory -> vertex(s)" table.
            handler (Handler): handler of the measurements.
            measurements (OrderedSet[Measurement]): measurements.

        Returns:
            (list[GraphEdge]): new edges.
        """

        edge_factory = self._table[handler]
        vertices = factory_vertices_table[edge_factory]
        edges = edge_factory.create(graph, vertices, measurements)
        return edges

    def merge(self, state: State, graph: Graph) -> None:
        """Merges state with the graph.

        1) Create new vertices for the state.
        2) Create edges for the state.
        3) Add edges to the graph.

        Args:
            state (State): new state to be merged with the graph.
            graph (Graph): main graph.
        """
        factory_vertices_table = self._create_vertex_table(graph, state)
        storage: dict[Handler, OrderedSet[Measurement]] = state.data
        for handler, measurements in storage.items():
            edges = self._create_edges(graph, factory_vertices_table, handler, measurements)
            graph.add_edge(edges)
