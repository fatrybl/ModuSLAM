"""Tests for the GraphMerger class.

1) tests for the protected _create_vertex_table() method. 2) tests for the public
merge() method.
"""

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import UnaryEdge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.index_generator import IndexStorage
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate_state import (
    State,
)
from slam.frontend_manager.graph_builder.graph_merger import GraphMerger
from slam.utils.deque_set import DequeSet
from tests.frontend_manager.conftest import (
    BasicTestVertex,
    create_measurement,
    edge_factory,
    element,
    handler,
)


def test_create_vertex_table(handler, edge_factory):
    index_storage = IndexStorage()
    timestamp = 1

    merger = GraphMerger[BasicTestVertex, UnaryEdge]()
    # add new key-value pair to the protected table. Only for testing purposes.
    merger._table = {handler: edge_factory}

    table = merger._create_vertex_table(index_storage, timestamp)

    assert len(table) == 1

    result_edge_factory, vertices = list(table.items())[0]

    assert result_edge_factory == edge_factory
    assert vertices[0].timestamp == timestamp


def test_merge(element, handler, edge_factory):
    graph = Graph[BasicTestVertex, UnaryEdge]()

    # add new key-value pair to the protected table. Only for testing purposes.
    graph.vertex_storage._vertices_table.update({BasicTestVertex: DequeSet()})

    merger = GraphMerger[BasicTestVertex, UnaryEdge]()

    # add new key-value pair to the protected table. Only for testing purposes.
    merger._table = {handler: edge_factory}

    state = State()
    z: Measurement = create_measurement(handler, element)
    state.add(z)

    merger.merge(state, graph)

    assert len(graph.vertex_storage.vertices) == 1
    assert graph.factor_graph.size() == 1

    vertex = graph.vertex_storage.get_vertices(BasicTestVertex)[0]

    assert vertex.timestamp == element.timestamp
    assert vertex.index == 0
    for edge in vertex.edges:
        assert isinstance(edge, UnaryEdge)
