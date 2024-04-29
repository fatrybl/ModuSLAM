import logging
from typing import Generic

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.index_generator import IndexStorage, generate_index
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.tables_initializer import init_handler_edge_factory_table
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class GraphMerger(Generic[GraphVertex, GraphEdge]):
    """Merges the graph candidate with the graph."""

    def __init__(self) -> None:
        self._table: dict[Handler, EdgeFactory] = {}

    @property
    def handler_edge_factory_table(self) -> dict[Handler, EdgeFactory]:
        """ "handler -> edge factory" table."""
        return self._table

    def init_table(self, config: dict[str, str]) -> None:
        """Initializes "handler -> edge factory" table.

        Args:
            config: "handler name -> edge factory name" pairs.

        Raises:
            ValueError: if the config is empty.
        """
        if config:
            self._table = init_handler_edge_factory_table(config)
        else:
            msg = "Empty config."
            logger.critical(msg)
            raise ValueError(msg)

    def merge(self, state: State, graph: Graph) -> None:
        """Merges the state with the graph.

        Args:
            state: a state to be merged with the graph.

            graph: a graph to merge the state with.
        """
        index_storage = graph.vertex_storage.index_storage
        storage: dict[Handler, OrderedSet[Measurement]] = state.data
        table = self._create_factory_vertices_table(index_storage, state.timestamp)

        for handler, measurements in storage.items():
            edge_factory = self._table[handler]
            vertices = table[edge_factory]

            edges = edge_factory.create(graph, vertices, measurements)
            graph.add_edges(edges)

    @staticmethod
    def _create_vertex(vertex_type: type[GraphVertex], index: int, timestamp: int) -> GraphVertex:
        """Creates vertex instances for the state.

        Args:
            vertex_type: type of the vertex.

            index: index of the vertex.

            timestamp: timestamp of the vertex.

        Returns:
            vertex.
        """
        vertex = vertex_type()
        vertex.index = index
        vertex.timestamp = timestamp
        return vertex

    def _create_factory_vertices_table(
        self, index_storage: IndexStorage, timestamp: int
    ) -> dict[EdgeFactory, list[GraphVertex]]:
        """Creates "edge factory -> vertices" table.

        Args:
            index_storage: storage with vertices` indices.

            timestamp: timestamp.

        Returns:
            "edge factory -> vertices" table.
        """

        table: dict[EdgeFactory, list[GraphVertex]] = {}
        edge_factories = self._table.values()

        vertices_types = set[type[GraphVertex]]()
        type_instance_table = dict[type[GraphVertex], GraphVertex]()
        vertices_types = vertices_types.union(
            *(factory.vertices_types for factory in edge_factories)
        )
        for v_type in vertices_types:
            index: int = generate_index(index_storage)
            vertex = self._create_vertex(v_type, index, timestamp)
            type_instance_table[v_type] = vertex

        for factory in edge_factories:
            vertices = [type_instance_table[v_type] for v_type in factory.vertices_types]
            table[factory] = vertices

        return table
