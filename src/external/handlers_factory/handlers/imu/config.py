from dataclasses import dataclass


@dataclass
class ImuHandlerConfig:
    """Configuration for IMU data preprocessor."""

    sensor_name: str
    data_reader: str  # declares the parser for the IMU data.
