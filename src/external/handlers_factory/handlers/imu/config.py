from dataclasses import dataclass

from src.moduslam.data_manager.batch_factory.configs import DataReaders


@dataclass
class ImuHandlerConfig:
    """Configuration for IMU data preprocessor."""

    sensor_name: str
    data_reader: str  # declares parser for the IMU data.


@dataclass
class KaistImuHandlerConfig(ImuHandlerConfig):
    """Configuration for KAIST IMU data preprocessor."""

    data_reader: str = DataReaders.kaist_urban


@dataclass
class TumVieImuHandlerConfig(ImuHandlerConfig):
    """Configuration for TUM VIE IMU data preprocessor."""

    data_reader: str = DataReaders.tum_vie


@dataclass
class Ros2ImuHandlerConfig(ImuHandlerConfig):
    """Configuration for S3E IMU data preprocessor."""

    data_reader: str = DataReaders.ros2
