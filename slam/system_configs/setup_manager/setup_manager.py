from dataclasses import dataclass

from slam.system_configs.setup_manager.edge_factories_initializer import (
    EdgeFactoriesInitializerConfig,
)
from slam.system_configs.setup_manager.handlers_factory import HandlersFactoryConfig
from slam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from slam.system_configs.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)


@dataclass
class SetupManagerConfig:
    """Setup manager configuration."""

    sensors_factory: SensorFactoryConfig
    handlers_factory: HandlersFactoryConfig
    edge_factories_initializer: EdgeFactoriesInitializerConfig
    state_analyzers_factory: StateAnalyzersFactoryConfig
