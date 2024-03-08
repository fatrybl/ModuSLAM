import logging

from system_configs.system.setup_manager.setup_manager import SetupManagerConfig

from slam.setup_manager.sensors_factory.factory import SensorFactory

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
        # HandlerFactory.init_handlers(cfg.handlers_factory)
        # StateAnalyzerFactory.init_analyzers(cfg.state_analyzers_factory)
        logger.debug("Setup Manager has been successfully configured")
