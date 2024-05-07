"""The module contains functions for initializing tables with different connections."""

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzersFactory


def init_handler_state_analyzer_table(input_table: dict[str, str]) -> dict[Handler, StateAnalyzer]:
    """Creates "handler -> state analyzer" table for the given input table.

    Args:
        input_table: "handler name -> state analyzer name" table.

    Returns:
        "handler -> state analyzer" table.

    Raises:
        ValueError: if the input table is empty.
    """

    if not bool(input_table):
        raise ValueError("Empty config")

    output_table: dict[Handler, StateAnalyzer] = {}
    for handler_name, analyzer_name in input_table.items():
        handler: Handler = HandlersFactory.get_handler(handler_name)
        analyzer: StateAnalyzer = StateAnalyzersFactory.get_analyzer(analyzer_name)
        output_table[handler] = analyzer
    return output_table


def init_handler_edge_factory_table(input_table: dict[str, str]) -> dict[Handler, EdgeFactory]:
    """Creates "handler -> edge factory" table for the given input table.

    Args:
        input_table: "handler name -> edge factory name" table.

    Returns:
        "handler -> edge factory" table.

    Raises:
        ValueError: if the input table is empty.
    """

    if not bool(input_table):
        raise ValueError("Empty config")

    output_table: dict[Handler, EdgeFactory] = {}
    for handler_name, edge_factory_name in input_table.items():
        handler: Handler = HandlersFactory.get_handler(handler_name)
        edge_factory: EdgeFactory = EdgeFactoriesInitializer.get_factory(edge_factory_name)
        output_table[handler] = edge_factory

    return output_table


def init_sensor_handler_table(input_table: dict[str, list[str]]) -> dict[Sensor, list[Handler]]:
    """Creates "sensor -> handlers" table for the given input table.

    Args:
        input_table: "sensor name -> list of handler names" table.

    Returns:
        "sensor -> handlers" table.

    Raises:
        ValueError: if the input table is empty.
    """

    if not bool(input_table):
        raise ValueError("Empty config")

    output_table: dict[Sensor, list[Handler]] = {}
    for sensor_name, handlers_names in input_table.items():
        sensor: Sensor = SensorsFactory.get_sensor(sensor_name)
        handlers = [HandlersFactory.get_handler(name) for name in handlers_names]
        output_table[sensor] = handlers

    return output_table
