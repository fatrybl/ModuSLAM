from dataclasses import dataclass

from configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)


@dataclass
class ImuOdometryFactoryConfig(EdgeFactoryConfig):
    """Config for Imu Preintegrated Odometry Edge Factory."""
