from typing import cast

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore

from moduslam.frontend_manager.graph_initializer.configs import (
    EdgeConfig,
    PriorImuBias,
    PriorLinearVelocity,
    PriorPose,
    PriorPosition,
)


def get_config() -> dict[str, EdgeConfig]:
    cs = ConfigStore.instance()
    cs.store(name="base_pose", node=PriorPose)
    cs.store(name="base_linear_velocity", node=PriorLinearVelocity)
    cs.store(name="base_imu_bias", node=PriorImuBias)
    cs.store(name="base_position", node=PriorPosition)

    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        config = cast(dict[str, EdgeConfig], cfg)  # avoid MyPy warnings

    return config
