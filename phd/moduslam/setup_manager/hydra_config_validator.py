import logging

from hydra.core.config_store import ConfigStore

from moduslam.logger.logging_config import main_manager
from phd.moduslam.setup_manager.sensors_factory.sensors_configs import (
    ImuConfig,
    Lidar3DConfig,
    StereoCameraConfig,
    VrsGpsConfig,
)

logger = logging.getLogger(main_manager)

cs = ConfigStore.instance()


def register_sensors_configs():
    cs.store(name="base_imu", node=ImuConfig)
    cs.store(name="base_lidar", node=Lidar3DConfig)
    cs.store(name="base_gps", node=VrsGpsConfig)
    cs.store(name="base_stereo_camera", node=StereoCameraConfig)


def register_config():
    """
    Registers base config_objects for Hydra validation schema:
    https://hydra.cc/docs/tutorials/structured_config/schema/
    """
    # cs.store(name="structured_schema_config", node=MainManagerConfig)
    # cs.store(group="datasets", name="base_kaist_dataset", node=KaistConfig)
    # cs.store(group="datasets", name="base_tum_vie_dataset", node=TumVieConfig)
    # cs.store(group="regimes", name="base_data_regime", node=DataRegimeConfig)
    # cs.store(group="handlers", name="base_kiss_icp_odometry", node=KissIcpScanMatcherConfig)
    # cs.store(group="handlers", name="base_vrs_gps_preprocessor", node=VrsGpsHandlerConfig)
    # cs.store(group="handlers", name="base_feature_detector", node=FeatureDetectorConfig)
    register_sensors_configs()
    # cs.store(group="map_factories", name="base_lidar_map_factory", node=LidarMapFactoryConfig)
    # cs.store(group="map_loaders", name="base_lidar_map_loader", node=LidarMapLoaderConfig)

    logger.debug("Structured config schema has been successfully registered.")
