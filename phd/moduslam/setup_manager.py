import logging

from phd.logger.logging_config import setup_manager
from phd.moduslam.sensors_factory.config_factory import get_config
from phd.moduslam.sensors_factory.factory import SensorsFactory

logger = logging.getLogger(setup_manager)


def setup_sensors() -> None:
    """Initializes global Sensors Factory."""
    config = get_config()
    SensorsFactory.init_sensors(config)
    logger.debug("Sensors have been initialized.")
