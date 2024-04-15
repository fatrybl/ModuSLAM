from dataclasses import dataclass

from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)


@dataclass
class LidarOdometryFactoryConfig(EdgeFactoryConfig):
    """Config for lidar odometry Edge Factory."""
