from typing import cast

from hydra.core.config_store import ConfigStore

from hydra import compose, initialize
from src.moduslam.sensors_factory.configs import (
    ImuConfig,
    Lidar3DConfig,
    MonocularCameraConfig,
    SensorConfig,
    StereoCameraConfig,
    UltraWideBandConfig,
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
    cs.store(name="base_monocular_camera", node=MonocularCameraConfig)
    cs.store(name="base_vrs_gps", node=VrsGpsConfig)
    cs.store(name="base_ultra_wide_band", node=UltraWideBandConfig)

    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        config = cast(dict[str, SensorConfig], cfg)  # avoid MyPy warnings

    return config
