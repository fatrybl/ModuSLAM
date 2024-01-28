import logging

from configs.system.setup_manager.setup_manager import SetupManagerConfig
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory

logger = logging.getLogger(__name__)


class SetupManager:
    """Main class for system setup. Defaults to MetaSingleton."""

    def __init__(self, cfg: SetupManagerConfig) -> None:
        """
        Args:
            cfg (SetupManagerConfig): config for setup manager.
        """
        SensorFactory.init_sensors(cfg.sensor_factory)
        logger.debug("Setup Manager has been successfully configured")
