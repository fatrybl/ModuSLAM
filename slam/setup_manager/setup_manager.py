import logging

from slam.utils.meta_singleton import MetaSingleton
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from configs.system.setup_manager.setup_manager import SetupManager as SetupManagerConfig

logger = logging.getLogger(__name__)


class SetupManager(metaclass=MetaSingleton):
    """ Main class for system setup. Defaults to MetaSingleton."""

    def __init__(self, cfg: SetupManagerConfig) -> None:
        """
        Args:
            cfg (SetupManagerConfig): config for setup manager.
        """
        self.sensor_factory = SensorFactory(cfg.sensor_factory)
        logger.debug("Setup Manager has been successfully configured")
