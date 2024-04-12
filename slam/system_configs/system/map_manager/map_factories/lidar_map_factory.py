from dataclasses import dataclass


@dataclass
class LidarMapFactoryConfig:
    num_channels: int = 4
    min_range: float = 5
    max_range: float = 100
