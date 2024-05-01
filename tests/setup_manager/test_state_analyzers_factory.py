"""Tests for the StateAnalyzersFactory class."""

from unittest.mock import MagicMock, patch

import pytest

from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.setup_manager.state_analyzers_factory import factory as factory_module
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzersFactory
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.system_configs.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)
from slam.utils.exceptions import ItemNotFoundError


@pytest.fixture
def state_analyzer_config():
    return StateAnalyzerConfig(
        name="test_state_analyzer",
        module_name="test_module",
        type_name=LidarOdometryStateAnalyzer.__name__,
        handler_name="test_handler",
    )


@pytest.fixture
def factory_config(state_analyzer_config):
    return StateAnalyzersFactoryConfig(
        package_name="test_package",
        analyzers={state_analyzer_config.name: state_analyzer_config},
    )


def test_init_analyzers(factory_config, state_analyzer_config):
    with (
        patch.object(factory_module, "import_object", return_value=LidarOdometryStateAnalyzer),
        patch.object(HandlersFactory, "get_handler", return_value=MagicMock()),
    ):

        StateAnalyzersFactory.init_analyzers(factory_config)
        analyzer = StateAnalyzersFactory.get_analyzer(state_analyzer_config.name)
        assert isinstance(analyzer, LidarOdometryStateAnalyzer)


def test_get_analyzer(factory_config, state_analyzer_config):
    with (
        patch.object(factory_module, "import_object", return_value=LidarOdometryStateAnalyzer),
        patch.object(HandlersFactory, "get_handler", return_value=MagicMock()),
    ):

        StateAnalyzersFactory.init_analyzers(factory_config)
        analyzer = StateAnalyzersFactory.get_analyzer(state_analyzer_config.name)
        assert isinstance(analyzer, LidarOdometryStateAnalyzer)


def test_get_analyzer_not_found(factory_config):
    with (
        patch.object(factory_module, "import_object", return_value=LidarOdometryStateAnalyzer),
        patch.object(HandlersFactory, "get_handler", return_value=MagicMock()),
    ):

        StateAnalyzersFactory.init_analyzers(factory_config)
        with pytest.raises(ItemNotFoundError):
            StateAnalyzersFactory.get_analyzer("non_existent_analyzer")
