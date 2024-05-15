import logging

from hydra.core.config_store import ConfigStore

from slam.logger.logging_config import main_manager
from slam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.data_manager.batch_factory.regime import RegimeConfig
from slam.system_configs.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from slam.system_configs.main_manager import MainManagerConfig
from slam.system_configs.map_manager.map_manager import MapManagerConfig
from slam.system_configs.setup_manager.sensors import ImuConfig, Lidar3DConfig

logger = logging.getLogger(main_manager)


def register_config():
    """
    Registers base configs for Hydra validation schema:
    https://hydra.cc/docs/tutorials/structured_config/schema/
    """
    cs = ConfigStore.instance()
    cs.store(name="structured_schema_config", node=MainManagerConfig)
    cs.store(group="datasets", name="base_kaist_dataset", node=KaistConfig)
    cs.store(group="regimes", name="base_regime", node=RegimeConfig)
    cs.store(group="handlers", name="base_kiss_icp_odometry", node=KissIcpScanMatcherConfig)
    cs.store(group="sensors", name="base_lidar3D", node=Lidar3DConfig)
    cs.store(group="sensors", name="base_imu", node=ImuConfig)
    cs.store(group="map_manager", name="base_map_manager", node=MapManagerConfig)

    logger.debug("Structured config schema has been successfully registered.")
