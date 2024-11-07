"""Configuration for IMU data preprocessor."""

from dataclasses import dataclass


@dataclass
class ImuHandlerConfig:
    sensor_name: str
