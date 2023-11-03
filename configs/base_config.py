from dataclasses import dataclass, field

from configs.system.data_manager.data_manager import DataManagerConfig
from configs.system.setup_manager.setup_manager import SetupManagerConfig


@dataclass
class BaseConfig:
    """
    Base configuration of the system. Cannot be used directly.
    To be overridden by other configs only.
    """
    setup_manager: SetupManagerConfig = field(
        default_factory=SetupManagerConfig)
    data_manager: DataManagerConfig = field(default_factory=DataManagerConfig)
