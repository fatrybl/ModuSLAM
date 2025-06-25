from dataclasses import dataclass


@dataclass
class LidarPointCloudConfig:
    """Lidar point cloud map factory configuration."""

    num_channels: int = 4  # x, y, z, intensity
    min_range: float | None = None
    max_range: float | None = None
