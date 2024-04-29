from dataclasses import dataclass

from slam.system_configs.data_manager.data_manager import DataManagerConfig
from slam.system_configs.frontend_manager.frontend_manager import FrontendManagerConfig
from slam.system_configs.map_manager.map_manager import MapManagerConfig
from slam.system_configs.setup_manager.setup_manager import SetupManagerConfig


@dataclass
class MainManagerConfig:
    """Base configuration of the system."""

    setup_manager: SetupManagerConfig
    data_manager: DataManagerConfig
    frontend_manager: FrontendManagerConfig
    map_manager: MapManagerConfig
