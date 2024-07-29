"""Tests for the GraphMerger class."""

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.edge_factories.interface import EdgeFactory
from moduslam.frontend_manager.graph.base_edges import UnaryEdge
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    State,
)
from moduslam.frontend_manager.graph_builder.graph_merger import GraphMerger
from moduslam.frontend_manager.handlers.interface import Handler
from moduslam.utils.ordered_set import OrderedSet
from tests.frontend_manager.conftest import edge_factory, element, handler
from tests.frontend_manager.objects import BasicTestVertex, create_measurement


def test_merge(element: Element, handler: Handler, edge_factory: EdgeFactory):
    graph = Graph[BasicTestVertex, UnaryEdge]()
    # add new key-value pair to the protected table. Only for testing purposes.
    graph.vertex_storage._vertices_table.update({BasicTestVertex: OrderedSet()})

    merger = GraphMerger[BasicTestVertex, UnaryEdge]()
    # add new key-value pair to the protected table. Only for testing purposes.
    merger._table = {handler: edge_factory}

    state = State()
    z = create_measurement(handler, element)
    state.add(z)

    merger.merge(state, graph)

    assert len(graph.vertex_storage.vertices) == 1
    assert graph.factor_graph.size() == 1

    vertex = graph.vertex_storage.get_vertices(BasicTestVertex)[0]

    assert vertex.timestamp == element.timestamp
    assert vertex.index == 0

    edges = graph.get_connected_edges(vertex)

    assert edges is not None
    for edge in edges:
        assert isinstance(edge, UnaryEdge)
