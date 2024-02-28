from dataclasses import dataclass

from system_configs.system.setup_manager.handlers_factory import HandlersFactoryConfig
from system_configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from system_configs.system.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)


@dataclass
class SetupManagerConfig:
    """Config for SetupManager."""

    sensors_factory: SensorFactoryConfig
    handlers_factory: HandlersFactoryConfig
    state_analyzers_factory: StateAnalyzersFactoryConfig
