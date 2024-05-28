from dataclasses import dataclass

from moduslam.system_configs.data_manager.data_manager import DataManagerConfig
from moduslam.system_configs.frontend_manager.frontend_manager import (
    FrontendManagerConfig,
)
from moduslam.system_configs.logger.config import LoggerConfig
from moduslam.system_configs.map_manager.map_manager import MapManagerConfig
from moduslam.system_configs.setup_manager.setup_manager import SetupManagerConfig


@dataclass
class MainManagerConfig:
    """Base configuration of the system."""

    setup_manager: SetupManagerConfig
    data_manager: DataManagerConfig
    frontend_manager: FrontendManagerConfig
    map_manager: MapManagerConfig
    logger: LoggerConfig
