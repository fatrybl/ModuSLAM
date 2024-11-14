import logging
from typing import cast

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore

from phd.logger.logging_config import setup_manager
from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from phd.moduslam.setup_manager.sensors_factory.sensors_configs import (
    ImuConfig,
    Lidar3DConfig,
    SensorConfig,
    StereoCameraConfig,
)

logger = logging.getLogger(setup_manager)


def register_configs():
    cs = ConfigStore.instance()
    cs.store(name="base_lidar3D", node=Lidar3DConfig)
    cs.store(name="base_imu", node=ImuConfig)
    cs.store(name="base_stereo_camera", node=StereoCameraConfig)


register_configs()


class SetupManager:
    """Sets up SLAM system before start."""

    def __init__(self) -> None:

        with initialize(version_base=None, config_path="sensors_factory/configs"):
            cfg = compose(config_name="config")
            config = cast(dict[str, SensorConfig], cfg)  # avoid MyPy warnings
            SensorsFactory.init_sensors(config)
            logger.debug("Setup Manager has been configured.")
