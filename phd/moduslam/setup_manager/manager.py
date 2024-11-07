import logging

from moduslam.logger.logging_config import setup_manager
from phd.moduslam.setup_manager.config import SetupManagerConfig
from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory

logger = logging.getLogger(setup_manager)


class SetupManager:
    """Sets up SLAM system before start."""

    def __init__(self, config: SetupManagerConfig) -> None:
        """
        Args:
            config: configuration of the SetupManager.
        """
        SensorsFactory.init_sensors(config.sensors_factory)
        logger.debug("Setup Manager has been configured.")
