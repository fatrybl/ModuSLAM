import logging

from phd.logger.logging_config import setup_manager
from phd.moduslam.setup_manager.sensors_factory.config_factory import get_config
from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory

logger = logging.getLogger(setup_manager)


class SetupManager:
    """ModuSLAM system setup."""

    def __init__(self) -> None:

        config = get_config()
        SensorsFactory.init_sensors(config)
        logger.debug("Setup Manager has been configured.")
