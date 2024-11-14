from dataclasses import dataclass

from phd.moduslam.frontend_manager.graph_initializer.config_objects import (
    InitializerConfig,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.config import (
    ImuHandlerConfig,
)
from phd.moduslam.frontend_manager.handlers.scan_matcher.config import (
    KissIcpScanMatcherConfig,
)
from phd.moduslam.frontend_manager.handlers.vrs_gps.config import VrsGpsHandlerConfig


@dataclass
class FrontendManagerConfig:
    """Base frontend manager configuration."""

    handlers: tuple[
        ImuHandlerConfig,
        VrsGpsHandlerConfig,
        KissIcpScanMatcherConfig,
        KissIcpScanMatcherConfig,
    ]
    graph_initializer: InitializerConfig
