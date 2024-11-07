from dataclasses import dataclass

from phd.moduslam.setup_manager.sensors_factory.config import SensorsFactoryConfig


@dataclass
class SetupManagerConfig:
    """Setup manager configuration."""

    sensors_factory: SensorsFactoryConfig
