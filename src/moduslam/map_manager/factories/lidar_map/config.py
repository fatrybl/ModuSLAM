from dataclasses import dataclass


@dataclass
class LidarPointCloudConfig:
    """Lidar point cloud map factory configuration."""

    num_channels: int = 4
    min_range: float = 3
    max_range: float = 120
