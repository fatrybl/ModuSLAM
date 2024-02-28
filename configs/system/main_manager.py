from dataclasses import dataclass

from configs.system.data_manager.data_manager import DataManagerConfig
from configs.system.setup_manager.setup_manager import SetupManagerConfig


@dataclass
class MainManagerConfig:
    """Base configuration of the system.

    Cannot be used directly. To be overridden by other configs only.
    """

    setup_manager: SetupManagerConfig
    data_manager: DataManagerConfig
