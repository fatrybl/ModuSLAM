from dataclasses import dataclass

from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)


@dataclass
class EdgeFactoriesInitializerConfig:
    package_name: str
    edge_factories: dict[str, EdgeFactoryConfig]
