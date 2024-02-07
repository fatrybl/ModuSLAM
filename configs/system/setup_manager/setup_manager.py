from dataclasses import dataclass, field

from configs.system.setup_manager.handler_factory import HandlerFactoryConfig
from configs.system.setup_manager.sensor_factory import SensorFactoryConfig


@dataclass
class SetupManagerConfig:
    """
    Config for SetupManager.
    """

    sensor_factory: SensorFactoryConfig = field(default_factory=SensorFactoryConfig)
    handler_factory: HandlerFactoryConfig = field(default_factory=HandlerFactoryConfig)
