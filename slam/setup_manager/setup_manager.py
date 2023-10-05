import logging

from slam.utils.meta_singleton import MetaSingleton
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from configs.system.setup_manager.setup import SetupManager as SetupManagerConfig

logger = logging.getLogger(__name__)


class SetupManager(metaclass=MetaSingleton):
    def __init__(self, cfg: SetupManagerConfig) -> None:
        self.sensor_factory = SensorFactory(cfg)
        logger.debug("Setup Manager has been successfully configured")
