from dataclasses import dataclass


@dataclass
class ImuHandlerConfig:
    """Configuration for IMU data preprocessor."""

    sensor_name: str
