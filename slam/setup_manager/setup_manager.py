import logging

from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.state_analyzers_factory.factory import StateAnalyzersFactory
from slam.system_configs.setup_manager.setup_manager import SetupManagerConfig

logger = logging.getLogger(__name__)


class SetupManager:
    """Sets up SLAM system before start."""

    def __init__(self, config: SetupManagerConfig) -> None:
        """
        Args:
            config: configuration of the SetupManager.
        """
        SensorsFactory.init_sensors(config.sensors_factory)
        HandlersFactory.init_handlers(config.handlers_factory)
        EdgeFactoriesInitializer.init_factories(config.edge_factories_initializer)
        StateAnalyzersFactory.init_analyzers(config.state_analyzers_factory)
        logger.debug("Setup Manager has been successfully configured")
