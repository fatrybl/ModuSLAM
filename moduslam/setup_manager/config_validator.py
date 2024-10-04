import logging

from hydra.core.config_store import ConfigStore

from moduslam.logger.logging_config import main_manager
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import Ros2Config
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import DataRegimeConfig
from moduslam.system_configs.frontend_manager.handlers.lidar_odometry import (
    KissIcpScanMatcherConfig,
)
from moduslam.system_configs.frontend_manager.handlers.visual_odometry import (
    FeatureDetectorConfig,
)
from moduslam.system_configs.frontend_manager.handlers.vrs_gps import (
    VrsGpsHandlerConfig,
)
from moduslam.system_configs.main_manager import MainManagerConfig
from moduslam.system_configs.map_manager.map_factories.lidar_map import (
    LidarMapFactoryConfig,
)
from moduslam.system_configs.map_manager.map_loaders.lidar_map import (
    LidarMapLoaderConfig,
)
from moduslam.system_configs.setup_manager.sensors import (
    ImuConfig,
    Lidar3DConfig,
    StereoCameraConfig,
)

logger = logging.getLogger(main_manager)


def register_config():
    """
    Registers base configs for Hydra validation schema:
    https://hydra.cc/docs/tutorials/structured_config/schema/
    """
    cs = ConfigStore.instance()
    cs.store(name="structured_schema_config", node=MainManagerConfig)
    cs.store(group="datasets", name="base_kaist_dataset", node=KaistConfig)
    cs.store(group="datasets", name="base_tum_vie_dataset", node=TumVieConfig)
    cs.store(group="datasets", name="base_ros2_dataset", node=Ros2Config)
    cs.store(group="regimes", name="base_data_regime", node=DataRegimeConfig)
    cs.store(group="handlers", name="base_kiss_icp_odometry", node=KissIcpScanMatcherConfig)
    cs.store(group="handlers", name="base_vrs_gps_preprocessor", node=VrsGpsHandlerConfig)
    cs.store(group="handlers", name="base_feature_detector", node=FeatureDetectorConfig)
    cs.store(group="sensors", name="base_lidar3D", node=Lidar3DConfig)
    cs.store(group="sensors", name="base_imu", node=ImuConfig)
    cs.store(group="sensors", name="base_stereo_camera", node=StereoCameraConfig)
    cs.store(group="map_factories", name="base_lidar_map_factory", node=LidarMapFactoryConfig)
    cs.store(group="map_loaders", name="base_lidar_map_loader", node=LidarMapLoaderConfig)

    logger.debug("Structured config schema has been successfully registered.")
