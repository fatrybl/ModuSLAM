from dataclasses import dataclass


@dataclass
class LidarPointCloudConfig:
    """Lidar pointcloud map factory configuration."""

    num_channels: int = 4
    min_range: float = 5
    max_range: float = 100
