from dataclasses import dataclass, field

from configs.system.setup_manager.handlers_factory import HandlerFactoryConfig
from configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from configs.system.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)


@dataclass
class SetupManagerConfig:
    """
    Config for SetupManager.
    """

    sensor_factory: SensorFactoryConfig = field(default_factory=SensorFactoryConfig)
    handler_factory: HandlerFactoryConfig = field(default_factory=HandlerFactoryConfig)
    state_analyzers_factory: StateAnalyzersFactoryConfig = field(default_factory=StateAnalyzersFactoryConfig)
