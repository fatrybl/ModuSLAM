from dataclasses import dataclass, field

from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig
from configs.system.setup_manager.setup_manager import SetupManagerConfig
from configs.system.frontend_manager.frontend_manager import FrontendManagerConfig
from configs.system.backend_manager.backend_manager import BackendManagerConfig
from configs.system.map_manager.map_manager import MapManagerConfig


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
    frontend_manager: FrontendManagerConfig = field(
        default_factory=FrontendManagerConfig)
    backend_manager: BackendManagerConfig = field(
        default_factory=BackendManagerConfig)
    map_manager: MapManagerConfig = field(
        default_factory=MapManagerConfig)
