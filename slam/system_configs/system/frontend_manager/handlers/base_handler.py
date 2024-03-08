from dataclasses import dataclass


@dataclass
class HandlerConfig:
    """Base config for a handler."""

    name: str
    type_name: str
    module_name: str


@dataclass
class KissIcpScanMatcherConfig(HandlerConfig):
    type_name: str = "ScanMatcher"
    module_name: str = ".pointcloud_matcher"
    name: str = "KissICP"
    max_points_per_voxel: int = 20
    voxel_size: float = 1.0
    adaptive_initial_threshold: float = 3.0
    min_range: float = 20
    max_range: float = 120
    deskew: bool = False
    preprocess: bool = True
