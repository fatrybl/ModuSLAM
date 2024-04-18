"""Tests for the tables_initializer module."""

from unittest.mock import MagicMock, patch

import pytest

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
from slam.setup_manager.tables_initializer import (
    init_handler_edge_factory_table,
    init_handler_state_analyzer_table,
    init_sensor_handler_table,
)


def test_init_handler_state_analyzer_table():
    # Mocking the Handler and StateAnalyzer objects
    mock_handler1 = MagicMock(spec=Handler)
    mock_handler2 = MagicMock(spec=Handler)
    mock_analyzer1 = MagicMock(spec=StateAnalyzer)
    mock_analyzer2 = MagicMock(spec=StateAnalyzer)

    config = {
        "handler1": "analyzer1",
        "handler2": "analyzer2",
    }

    with (
        patch.object(HandlersFactory, "get_handler") as mock_get_handler,
        patch.object(StateAnalyzersFactory, "get_analyzer") as mock_get_analyzer,
    ):

        # Setting the return values for the mocked methods
        mock_get_handler.side_effect = [mock_handler1, mock_handler2]
        mock_get_analyzer.side_effect = [mock_analyzer1, mock_analyzer2]

        # Calling the function to test
        result = init_handler_state_analyzer_table(config)

        # Checking if the mocked methods were called with the correct arguments
        mock_get_handler.assert_any_call("handler1")
        mock_get_handler.assert_any_call("handler2")
        mock_get_analyzer.assert_any_call("analyzer1")
        mock_get_analyzer.assert_any_call("analyzer2")

        # Checking if the function returned the expected result
        assert result == {
            mock_handler1: mock_analyzer1,
            mock_handler2: mock_analyzer2,
        }


def test_init_handler_state_analyzer_table_empty_config():
    config: dict = {}

    with pytest.raises(ValueError, match="Empty config"):
        init_handler_state_analyzer_table(config)


def test_init_handler_edge_factory_table():
    # Mocking the Handler and EdgeFactory objects
    mock_handler1 = MagicMock(spec=Handler)
    mock_handler2 = MagicMock(spec=Handler)
    mock_edge_factory1 = MagicMock(spec=EdgeFactory)
    mock_edge_factory2 = MagicMock(spec=EdgeFactory)

    config = {
        "handler1": "edge_factory1",
        "handler2": "edge_factory2",
    }

    with (
        patch.object(HandlersFactory, "get_handler") as mock_get_handler,
        patch.object(EdgeFactoriesInitializer, "get_factory") as mock_get_factory,
    ):

        # Setting the return values for the mocked methods
        mock_get_handler.side_effect = [mock_handler1, mock_handler2]
        mock_get_factory.side_effect = [mock_edge_factory1, mock_edge_factory2]

        result = init_handler_edge_factory_table(config)

        # Checking if the mocked methods were called with the correct arguments
        mock_get_handler.assert_any_call("handler1")
        mock_get_handler.assert_any_call("handler2")
        mock_get_factory.assert_any_call("edge_factory1")
        mock_get_factory.assert_any_call("edge_factory2")

        # Checking if the function returned the expected result
        assert result == {
            mock_handler1: mock_edge_factory1,
            mock_handler2: mock_edge_factory2,
        }


def test_init_handler_edge_factory_table_empty_config():
    config: dict = {}

    with pytest.raises(ValueError, match="Empty config"):
        init_handler_edge_factory_table(config)


def test_init_sensor_handler_table():
    mock_sensor1 = MagicMock(spec=Sensor)
    mock_handler1 = MagicMock(spec=Handler)
    mock_handler2 = MagicMock(spec=Handler)

    config = {
        "sensor1": ["handler1", "handler2"],
    }

    with (
        patch.object(SensorsFactory, "get_sensor") as mock_get_sensor,
        patch.object(HandlersFactory, "get_handler") as mock_get_handler,
    ):

        # Setting the return values for the mocked methods
        mock_get_sensor.return_value = mock_sensor1
        mock_get_handler.side_effect = [mock_handler1, mock_handler2]

        result = init_sensor_handler_table(config)

        # Checking if the mocked methods were called with the correct arguments
        mock_get_sensor.assert_called_once_with("sensor1")
        mock_get_handler.assert_any_call("handler1")
        mock_get_handler.assert_any_call("handler2")

        # Checking if the function returned the expected result
        assert result == {
            mock_sensor1: [mock_handler1, mock_handler2],
        }


def test_init_sensor_handler_table_empty_config():
    config: dict = {}

    with pytest.raises(ValueError, match="Empty config"):
        init_sensor_handler_table(config)
