from dataclasses import dataclass

from slam.system_configs.system.setup_manager.edge_factories_initializer import (
    EdgeFactoriesInitializerConfig,
)
from slam.system_configs.system.setup_manager.handlers_factory import (
    HandlersFactoryConfig,
)
from slam.system_configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from slam.system_configs.system.setup_manager.state_analyzers_factory import (
    StateAnalyzerFactoryConfig,
)


@dataclass
class SetupManagerConfig:
    """Config for SetupManager."""

    sensors_factory: SensorFactoryConfig
    handlers_factory: HandlersFactoryConfig
    edge_factories_initializer: EdgeFactoriesInitializerConfig
    state_analyzers_factory: StateAnalyzerFactoryConfig
