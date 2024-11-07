from dataclasses import dataclass

from moduslam.system_configs.data_manager.data_manager import DataManagerConfig
from moduslam.system_configs.logger.config import LoggerConfig
from moduslam.system_configs.map_manager.map_manager import MapManagerConfig
from phd.moduslam.frontend_manager.base_config import FrontendManagerConfig
from phd.moduslam.setup_manager.config import SetupManagerConfig


@dataclass
class MainManagerConfig:
    """Base configuration of the system."""

    setup_manager: SetupManagerConfig
    data_manager: DataManagerConfig
    frontend_manager: FrontendManagerConfig
    map_manager: MapManagerConfig
    logger: LoggerConfig
