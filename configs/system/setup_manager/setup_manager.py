from dataclasses import dataclass, field

from .sensor_factory import SensorFactoryConfig


@dataclass
class SetupManagerConfig:
    """
    Config for SetupManager.
    """
    sensor_factory: SensorFactoryConfig = field(
        default_factory=SensorFactoryConfig)
