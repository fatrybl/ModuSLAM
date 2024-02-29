from dataclasses import dataclass

from slam.system_configs.system.data_manager.data_manager import DataManagerConfig
from slam.system_configs.system.setup_manager.setup_manager import SetupManagerConfig


@dataclass
class MainManagerConfig:
    """Base configuration of the system.

    Cannot be used directly. To be overridden by other system_configs only.
    """

    setup_manager: SetupManagerConfig
    data_manager: DataManagerConfig
