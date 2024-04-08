import pytest

from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


@pytest.fixture
def state_analyzer_config():
    return StateAnalyzerConfig(
        name="test_state_analyzer",
        handler_name="test_handler",
        type_name="test_type",
        module_name="test_module",
    )


@pytest.fixture
def state_analyzer(state_analyzer_config):
    return LidarOdometryStateAnalyzer(state_analyzer_config)
