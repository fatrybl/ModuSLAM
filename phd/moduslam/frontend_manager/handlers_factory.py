import logging
from dataclasses import dataclass
from typing import cast

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING

from phd.logger.logging_config import data_manager
from phd.moduslam.frontend_manager.handlers.camera_features_detector.config import (
    FeatureDetectorConfig,
)
from phd.moduslam.frontend_manager.handlers.handler_protocol import Handler
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.config import (
    ImuHandlerConfig,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.kaist_urban_handler import (
    KaistUrbanImuDataPreprocessor,
)
from phd.moduslam.frontend_manager.handlers.scan_matcher.config import (
    KissIcpScanMatcherConfig,
)
from phd.moduslam.frontend_manager.handlers.scan_matcher.handler import ScanMatcher
from phd.moduslam.frontend_manager.handlers.vrs_gps.config import VrsGpsHandlerConfig
from phd.moduslam.frontend_manager.handlers.vrs_gps.handler import (
    KaistUrbanVrsGpsPreprocessor,
)

logger = logging.getLogger(data_manager)


@dataclass
class Handlers:
    scan_matcher1: KissIcpScanMatcherConfig = MISSING
    scan_matcher2: KissIcpScanMatcherConfig = MISSING
    imu_preprocessor: ImuHandlerConfig = MISSING
    vrs_preprocessor: VrsGpsHandlerConfig = MISSING


def register_configs():
    cs = ConfigStore.instance()
    cs.store(name="base_handlers_factory", node=Handlers)
    cs.store(group="handlers", name="base_imu_preprocessor", node=ImuHandlerConfig)
    cs.store(group="handlers", name="base_scan_matcher", node=KissIcpScanMatcherConfig)
    cs.store(group="handlers", name="base_camera_features_detector", node=FeatureDetectorConfig)
    cs.store(group="handlers", name="base_vrs_gps_preprocessor", node=VrsGpsHandlerConfig)


register_configs()


class Factory:

    _handlers: set[Handler] = set()

    @classmethod
    def init_handlers(cls) -> None:
        """Initializes handlers."""

        with initialize(version_base=None, config_path="configs"):
            cfg = compose(config_name="config")
            config = cast(Handlers, cfg)  # avoid MyPy warnings

        scan_matcher1 = ScanMatcher(config.scan_matcher1)
        scan_matcher2 = ScanMatcher(config.scan_matcher2)
        imu_preprocessor = KaistUrbanImuDataPreprocessor(config.imu_preprocessor)
        vrs_gps_preprocessor = KaistUrbanVrsGpsPreprocessor(config.vrs_preprocessor)

        cls._handlers = {scan_matcher1, scan_matcher2, imu_preprocessor, vrs_gps_preprocessor}

        logger.debug("All handlers have been configured.")

    @classmethod
    def get_handlers(cls) -> set[Handler]:
        """Gets all handlers."""
        return cls._handlers
