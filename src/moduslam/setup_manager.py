import logging

from src.logger.logging_config import setup_manager
from src.moduslam.sensors_factory.config_factory import get_config
from src.moduslam.sensors_factory.factory import SensorsFactory

logger = logging.getLogger(setup_manager)


def setup_sensors() -> None:
    """Initializes global Sensors Factory."""
    config = get_config()  # Hydra does not support lists -> we use dictionaries.
    SensorsFactory.init_sensors(config.values())
    logger.debug("Sensors have been initialized.")
