from dataclasses import dataclass

from system_configs.system.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class StereoSmartFeaturesConfig(HandlerConfig):
    """Config for Stereo Smart Features."""
