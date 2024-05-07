from dataclasses import dataclass

from slam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)


@dataclass
class EdgeFactoriesInitializerConfig:
    """Edge factories initializer configuration."""

    package_name: str
    edge_factories: dict[str, EdgeFactoryConfig]
