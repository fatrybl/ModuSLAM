from dataclasses import dataclass

from slam.system_configs.system.frontend_manager.handlers.base_handler import (
    HandlerConfig,
)


@dataclass
class KissIcpScanMatcherConfig(HandlerConfig):
    type_name: str = "ScanMatcher"
    module_name: str = ".pointcloud_matcher"
    name: str = "kiss_icp_odometry"
    max_points_per_voxel: int = 10
    voxel_size: float = 1.5
    adaptive_initial_threshold: float = 3.0
    min_range: float = 10
    max_range: float = 100
    deskew: bool = False
    preprocess: bool = False
    measurement_noise_covariance: tuple[float, ...] = (1, 1, 1, 1, 1, 1)
