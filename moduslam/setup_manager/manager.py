import logging

from moduslam.logger.logging_config import setup_manager
from moduslam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from moduslam.setup_manager.handlers_factory.factory import HandlersFactory
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.state_analyzers_factory.factory import StateAnalyzersFactory
from moduslam.system_configs.setup_manager.setup_manager import SetupManagerConfig

logger = logging.getLogger(setup_manager)


class SetupManager:
    """Sets up SLAM system before start."""

    def __init__(self, config: SetupManagerConfig) -> None:
        """
        Args:
            config: configuration of the SetupManager.
        """
        print("CONFIGURATION FOR SENSORS IS:")
        for sensors in config.sensors_factory.values():
            for sensor, value in sensors.items():
                print(sensor, value)

        SensorsFactory.init_sensors(config.sensors_factory)
        HandlersFactory.init_handlers(config.handlers_factory)
        EdgeFactoriesInitializer.init_factories(config.edge_factories_initializer)
        StateAnalyzersFactory.init_analyzers(config.state_analyzers_factory)
        logger.debug("Setup Manager has been configured.")
