import logging

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.index_generator import IndexStorage, generate_index
from slam.frontend_manager.graph.vertices import Vertex
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.handlers_factory.factory import HandlerFactory
from slam.system_configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class GraphMerger:
    """Merges the graph candidate with the main graph."""

    def __init__(self, config: GraphMergerConfig) -> None:
        self._table: dict[Handler, EdgeFactory] = {}
        self._fill_table(config.handler_edge_factory_table)

    def _fill_table(self, config: dict[str, str]) -> None:
        """Fills in the table which represents handler -> edge factory connections.

        Args:
            config (dict[str, str]): configuration.
        """
        for handler_name, edge_factory_name in config.items():
            handler: Handler = HandlerFactory.get_handler(handler_name)
            edge_factory: EdgeFactory = EdgeFactoriesInitializer.get_factory(edge_factory_name)
            self._table[handler] = edge_factory

    @staticmethod
    def _create_vertex(
        index_storage: IndexStorage, vertex_type: type[Vertex], timestamp: int
    ) -> Vertex:
        """
        Creates a vertex instance for the given edge factory.
        Generates a unique index of the vertex for the given graph.
        Args:
            index_storage (IndexStorage): storage of unique indices.
            vertex_type (type[Vertex]): type of the vertex.
            timestamp (int): timestamp of the vertex.

        Returns:
            (Vertex): new vertex instance.
        """
        vertex: Vertex = vertex_type()
        vertex.index = generate_index(index_storage)
        vertex.timestamp = timestamp
        return vertex

    def _create_vertex_table(self, graph: Graph, state: State) -> dict[EdgeFactory, Vertex]:
        """
        Creates vertex instances for the state.
        The instances are empty: not initialized yet.

        Args:
            state (State): state with measurements.

        Returns:
            (dict[EdgeFactory, Vertex]): "Edge Factory -> Vertex" table.

        """

        vertices: dict[EdgeFactory, Vertex] = {}
        indices = graph.vertex_storage.index_storage
        timestamp = state.timestamp
        handlers = state.data.keys()

        for handler in handlers:
            edge_factory = self._table[handler]
            vertex = self._create_vertex(
                indices,
                edge_factory.vertex_type,
                timestamp,
            )
            vertices[edge_factory] = vertex

        return vertices

    def _create_edges(
        self, graph: Graph, state: State, vertex_table: dict[EdgeFactory, Vertex]
    ) -> list[Edge]:
        """
        Creates edges for the state.
        Note:
            Each handler is being processed by the corresponding edge factory.
            Every edge factory uses vertex of the given state.

        Args:
            graph (Graph): main graph.
            state (State): state with measurements.
            vertex_table (dict[EdgeFactory, Vertex]): "edge factory -> vertex" table.

        Returns:
            (list[Edge]): new edges.
        """
        edges: list[Edge] = []
        data: dict[Handler, OrderedSet[Measurement]] = state.data

        for handler, measurements in data.items():
            edge_factory = self._table[handler]
            vertex = vertex_table[edge_factory]
            new_edges = edge_factory.create(graph, vertex, measurements)
            vertex.edges.update(new_edges)
            edges += new_edges

        return edges

    @property
    def handler_edge_factory_table(self) -> dict[Handler, EdgeFactory]:
        """A table to represent the connections between handlers & edge factories.

        Returns:
            (dict[Handler, EdgeFactory]): handler -> edge factory table.
        """
        return self._table

    def merge(self, state: State, graph: Graph) -> None:
        """Merges state with the graph.

        1) Determine graph vertices for the state.
        2) Create edges for the state using determined vertices.
        3) Remove state measurements from the storage.

        Args:
            state (State): new state to be merged with the graph.
            graph (Graph): main graph.
        """
        vertex_table = self._create_vertex_table(graph, state)
        edges = self._create_edges(graph, state, vertex_table)
        graph.add_edge(edges)
