"""Matches measurement handlers with edges_123."""

from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.handlers.ABC_handler import Handler

handler_edge_table: dict[Handler, EdgeFactory] = {}
