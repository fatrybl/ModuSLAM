from dataclasses import dataclass, field

from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig
from configs.system.setup_manager.setup_manager import SetupManagerConfig


@dataclass
class BaseConfig:
    """
    Base configuration of the system. Cannot be used directly.
    To be overridden by other configs only.
    """
    setup_manager: SetupManagerConfig = field(
        default_factory=SetupManagerConfig)
    data_manager: BatchFactoryConfig = field(
        default_factory=BatchFactoryConfig)
