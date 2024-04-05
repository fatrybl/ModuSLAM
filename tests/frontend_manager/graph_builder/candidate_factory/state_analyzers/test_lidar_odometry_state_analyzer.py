from unittest.mock import patch

import pytest

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate_state import (
    State,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory


@pytest.fixture
def measurement_storage(measurement):
    storage = MeasurementStorage()
    storage.add(measurement)
    return storage


class TestLidarOdometryStateAnalyzer:
    def test_init(self, handler, state_analyzer_config):
        with patch.object(HandlersFactory, "get_handler", return_value=handler):
            analyzer = LidarOdometryStateAnalyzer(state_analyzer_config)
            assert isinstance(analyzer, LidarOdometryStateAnalyzer)

    def test_evaluate(self, handler, state_analyzer_config, measurement_storage):
        with patch.object(HandlersFactory, "get_handler", return_value=handler):
            analyzer = LidarOdometryStateAnalyzer(state_analyzer_config)
            state = analyzer.evaluate(measurement_storage)
            assert isinstance(state, State)
            assert state.data == measurement_storage.data
