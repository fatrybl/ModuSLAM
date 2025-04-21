import logging
from dataclasses import dataclass
from typing import cast

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING

from hydra import compose, initialize
from src.external.handlers_factory.handlers.handler_protocol import Handler
from src.external.handlers_factory.handlers.imu.config import (
    ImuHandlerConfig,
    Ros2ImuHandlerConfig,
)
from src.external.handlers_factory.handlers.imu.handler import (
    ImuHandler,
)
from src.external.handlers_factory.handlers.scan_matcher.config import (
    KissIcpScanMatcherConfig,
)
from src.external.handlers_factory.handlers.scan_matcher.handler import ScanMatcher
from src.external.handlers_factory.handlers.visual_odometry.handler import (
    VisualOdometryConfig,
)
from src.external.handlers_factory.handlers.vrs_gps.config import VrsGpsHandlerConfig
from src.logger.logging_config import data_manager

logger = logging.getLogger(data_manager)


@dataclass
class Handlers:
    """Measurement handlers configuration."""

    scan_matcher1: KissIcpScanMatcherConfig = MISSING
    scan_matcher2: KissIcpScanMatcherConfig = MISSING
    imu_preprocessor: ImuHandlerConfig = MISSING
    vrs_preprocessor: VrsGpsHandlerConfig = MISSING
    visual_odometry: VisualOdometryConfig = MISSING


def get_config() -> Handlers:
    """Gets configuration for measurement handlers.

    Returns:
        configurations.
    """
    cs = ConfigStore.instance()
    cs.store(name="base_handlers_factory", node=Handlers)
    cs.store(name="base_imu_preprocessor", node=Ros2ImuHandlerConfig)
    cs.store(name="base_scan_matcher", node=KissIcpScanMatcherConfig)
    cs.store(name="base_visual_odometry", node=VisualOdometryConfig)
    cs.store(name="base_vrs_gps_preprocessor", node=VrsGpsHandlerConfig)

    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        config = cast(Handlers, cfg)  # avoid MyPy warnings

    return config


class Factory:
    """Initializes and stores measurement handlers."""

    _handlers: set[Handler] = set()

    @classmethod
    def init_handlers(cls) -> None:
        """Initializes handlers."""

        config = get_config()

        scan_matcher1 = ScanMatcher(config.scan_matcher1)
        # scan_matcher2 = ScanMatcher(config.scan_matcher2)
        imu_preprocessor = ImuHandler(config.imu_preprocessor)
        # vrs_gps_preprocessor = KaistUrbanVrsGpsPreprocessor(config.vrs_preprocessor)
        # visual_odometry = VisualOdometry(config.visual_odometry)

        cls._handlers = {
            scan_matcher1,
            imu_preprocessor,
            # vrs_gps_preprocessor,
            # visual_odometry,
        }

        logger.debug("All handlers have been initialized.")

    @classmethod
    def get_handlers(cls) -> set[Handler]:
        """Gets all handlers.

        Returns:
            handlers.
        """
        return cls._handlers
