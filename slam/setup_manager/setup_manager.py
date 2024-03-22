import logging

from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.handlers_factory.factory import HandlerFactory
from slam.setup_manager.sensors_factory.factory import SensorFactory
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzerFactory
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
        SensorFactory.init_sensors(cfg.sensors_factory)
        HandlerFactory.init_handlers(cfg.handlers_factory)
        EdgeFactoriesInitializer.init_factories(cfg.edge_factories_initializer)
        StateAnalyzerFactory.init_analyzers(cfg.state_analyzers_factory)
        logger.debug("Setup Manager has been successfully configured")
