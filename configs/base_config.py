from dataclasses import dataclass, field

from configs.system.data_manager.data_manager import DataManager
from configs.system.setup_manager.setup_manager import SetupManager


@dataclass
class BaseConfig:
    """
    Base configuration of the system. Cannot be used directly.
    To be overridden by other configs only.
    """
    setup_manager: SetupManager = field(default_factory=SetupManager)
    data_manager: DataManager = field(default_factory=DataManager)
