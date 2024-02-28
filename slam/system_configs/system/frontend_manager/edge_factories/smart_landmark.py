from dataclasses import dataclass

from system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)


@dataclass
class SmartStereoFeaturesFactoryConfig(EdgeFactoryConfig):
    """Config for Smart Stereo Landmark Edge Factory."""
