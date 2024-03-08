from hydra.core.config_store import ConfigStore

from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import RegimeConfig
from slam.system_configs.system.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    LidarOdometryStateAnalyzerConfig,
)
from slam.system_configs.system.main_manager import MainManagerConfig


def register_config():
    cs = ConfigStore.instance()
    cs.store(name="structured_schema_config", node=MainManagerConfig)
    cs.store(group="datasets", name="base_kaist_dataset", node=KaistConfig)
    cs.store(group="regimes", name="base_regime", node=RegimeConfig)
    # cs.store(group="handlers", name="base_lidar_odometry", node=ScanMatcherConfig)
    cs.store(
        group="state_analyzers",
        name="base_lidar_odometry_state_analyzer",
        node=LidarOdometryStateAnalyzerConfig,
    )
