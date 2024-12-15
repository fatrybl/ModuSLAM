from typing import cast

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore

from phd.moduslam.setup_manager.sensors_factory.configs import (
    ImuConfig,
    Lidar3DConfig,
    SensorConfig,
    StereoCameraConfig,
    VrsGpsConfig,
)


def get_config() -> dict[str, SensorConfig]:
    """Registers base configs for Hydra validation schema:
    https://hydra.cc/docs/tutorials/structured_config/schema/
    """
    cs = ConfigStore.instance()
    cs.store(name="base_imu", node=ImuConfig)
    cs.store(name="base_lidar3D", node=Lidar3DConfig)
    cs.store(name="base_stereo_camera", node=StereoCameraConfig)
    cs.store(name="base_vrs_gps", node=VrsGpsConfig)

    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        config = cast(dict[str, SensorConfig], cfg)  # avoid MyPy warnings

    return config
