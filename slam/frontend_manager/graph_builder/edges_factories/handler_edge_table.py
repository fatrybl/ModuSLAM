"""Matches measurement handlers with edges_123."""

<<<<<<<< HEAD:slam/frontend_manager/graph_builder/edge_factories/handler_edge_table.py
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
========
from slam.frontend_manager.graph_builder.edges_factories.edge_factory_ABC import (
>>>>>>>> 3e68bcf (UPD: save current progress):slam/frontend_manager/graph_builder/edges_factories/handler_edge_table.py
    EdgeFactory,
)
from slam.frontend_manager.handlers.ABC_handler import Handler

handler_edge_table: dict[Handler, EdgeFactory] = {}
