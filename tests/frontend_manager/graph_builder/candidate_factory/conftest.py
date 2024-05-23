import pytest

from slam.frontend_manager.graph_builder.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


@pytest.fixture
def state_analyzer_config():
    return StateAnalyzerConfig(
        name="test_state_analyzer",
        type_name="test_type",
        module_name="test_module",
    )


@pytest.fixture
def state_analyzer(state_analyzer_config):
    return LidarOdometryStateAnalyzer(state_analyzer_config)
