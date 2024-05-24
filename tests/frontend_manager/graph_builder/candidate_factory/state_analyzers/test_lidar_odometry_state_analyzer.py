from unittest.mock import patch

from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate_state import (
    State,
)
from moduslam.frontend_manager.graph_builder.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from moduslam.setup_manager.handlers_factory.factory import HandlersFactory
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
        measurements = measurement_storage.data[handler]
        state = analyzer.evaluate(measurements)
        assert isinstance(state, State)
        assert state.data == measurement_storage.data
