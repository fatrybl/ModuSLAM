from unittest.mock import patch

from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate_state import (
    State,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from tests.frontend_manager.conftest import handler, measurement_storage
from tests.frontend_manager.graph_builder.candidate_factory.conftest import (
    state_analyzer_config,
)


def test_init(handler, state_analyzer_config):
    with patch.object(HandlersFactory, "get_handler", return_value=handler):
        analyzer = LidarOdometryStateAnalyzer(state_analyzer_config)
        assert isinstance(analyzer, LidarOdometryStateAnalyzer)


def test_evaluate(handler, state_analyzer_config, measurement_storage):
    with patch.object(HandlersFactory, "get_handler", return_value=handler):
        analyzer = LidarOdometryStateAnalyzer(state_analyzer_config)
        state = analyzer.evaluate(measurement_storage)
        assert isinstance(state, State)
        assert state.data == measurement_storage.data
