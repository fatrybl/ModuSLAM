from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.handlers_factory.factory import HandlerFactory
from slam.setup_manager.sensors_factory.factory import SensorFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzerFactory


def init_handler_analyze_table(config: dict[str, str]) -> dict[Handler, StateAnalyzer]:
    """Fills in the table which represents handler -> state analyzer connections.

    Args:
        config (dict[str, str): configuration: [handler_name: analyzer_name].

    Returns:
        (dict[Handler, StateAnalyzer]): table.
    """

    assert bool(config), "Empty config"

    table: dict[Handler, StateAnalyzer] = {}
    for handler_name, analyzer_name in config.items():
        handler: Handler = HandlerFactory.get_handler(handler_name)
        analyzer: StateAnalyzer = StateAnalyzerFactory.get_analyzer(analyzer_name)
        table[handler] = analyzer
    return table


def init_handler_edge_factory_table(config: dict[str, str]) -> dict[Handler, EdgeFactory]:
    """Fills in the table which represents handler -> edge factory connections.

    Args:
        config (dict[str, str]): configuration.

    Returns:
        (dict[Handler, EdgeFactory]): table.
    """
    assert bool(config), "Empty config"

    table: dict[Handler, EdgeFactory] = {}
    for handler_name, edge_factory_name in config.items():
        handler: Handler = HandlerFactory.get_handler(handler_name)
        edge_factory: EdgeFactory = EdgeFactoriesInitializer.get_factory(edge_factory_name)
        table[handler] = edge_factory

    return table


def init_sensor_handler_table(config: dict[str, list[str]]) -> dict[Sensor, list[Handler]]:
    """
    Fills in the table which represents sensor -> handlers connections.
    Args:
        config (dict[str, list[str]]): configuration.

    Returns:
        (dict[Sensor, list[Handler]]): table.
    """

    assert bool(config), "Empty config"

    table: dict[Sensor, list[Handler]] = {}
    for sensor_name, handlers_names in config.items():
        sensor: Sensor = SensorFactory.get_sensor(sensor_name)
        handlers = [HandlerFactory.get_handler(name) for name in handlers_names]
        table[sensor] = handlers

    return table
