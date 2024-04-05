import logging

from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzersFactory
from slam.system_configs.system.setup_manager.setup_manager import SetupManagerConfig

logger = logging.getLogger(__name__)


class SetupManager:
    """Main class for system setup.

    Defaults to MetaSingleton.
    """

    def __init__(self, cfg: SetupManagerConfig) -> None:
        """
        Args:
            cfg (SetupManagerConfig): config for setup manager.
        """
        SensorsFactory.init_sensors(cfg.sensors_factory)
        HandlersFactory.init_handlers(cfg.handlers_factory)
        EdgeFactoriesInitializer.init_factories(cfg.edge_factories_initializer)
        StateAnalyzersFactory.init_analyzers(cfg.state_analyzers_factory)
        logger.debug("Setup Manager has been successfully configured")
