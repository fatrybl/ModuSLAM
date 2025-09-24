from dataclasses import dataclass, field

from omegaconf import MISSING

from moduslam.sensors_factory.sensors import (
    Imu,
    Lidar3D,
    MonocularCamera,
    Sensor,
    StereoCamera,
    UltraWideBand,
    VrsGps,
)


@dataclass
class SensorConfig:
    """Base sensor configuration."""

    name: str
    sensor_type_name: str = Sensor.__name__


@dataclass
class MonocularCameraConfig(SensorConfig):
    sensor_type_name: str = MonocularCamera.__name__

    distortion_model: str = "plumb bob"
    camera_type: str = "pinhole"

    width: int = MISSING
    height: int = MISSING

    camera_matrix: list[list[float]] = MISSING

    distortion_coefficients: list[float] = MISSING

    rectification_matrix: list[list[float]] = MISSING

    projection_matrix: list[list[float]] = MISSING

    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


@dataclass
class StereoCameraConfig(SensorConfig):
    sensor_type_name: str = StereoCamera.__name__

    distortion_model_left: str = "plumb bob"
    distortion_model_right: str = "plumb bob"

    width: int = MISSING
    height: int = MISSING

    camera_matrix_left: list[list[float]] = MISSING

    camera_matrix_right: list[list[float]] = MISSING

    distortion_coefficients_left: list[float] = MISSING

    distortion_coefficients_right: list[float] = MISSING

    rectification_matrix_left: list[list[float]] = MISSING

    rectification_matrix_right: list[list[float]] = MISSING

    projection_matrix_left: list[list[float]] = MISSING

    projection_matrix_right: list[list[float]] = MISSING

    tf_left_right: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


@dataclass
class ImuConfig(SensorConfig):
    """IMU sensor configuration."""

    sensor_type_name: str = Imu.__name__

    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        metadata={"help": "Transformation matrix base link -> sensor."},
    )
    accelerometer_noise_covariance: list[list[float]] = field(
        default_factory=lambda: [
            [1e-3, 0.0, 0.0],
            [0.0, 1e-3, 0.0],
            [0.0, 0.0, 1e-3],
        ],
    )
    gyroscope_noise_covariance: list[list[float]] = field(
        default_factory=lambda: [
            [1e-3, 0.0, 0.0],
            [0.0, 1e-3, 0.0],
            [0.0, 0.0, 1e-3],
        ],
    )
    accelerometer_bias_noise_covariance: list[list[float]] = field(
        default_factory=lambda: [
            [1e-5, 0.0, 0.0],
            [0.0, 1e-5, 0.0],
            [0.0, 0.0, 1e-5],
        ],
    )
    gyroscope_bias_noise_covariance: list[list[float]] = field(
        default_factory=lambda: [
            [1e-5, 0.0, 0.0],
            [0.0, 1e-5, 0.0],
            [0.0, 0.0, 1e-5],
        ],
    )
    integration_noise_covariance: list[list[float]] = field(
        default_factory=lambda: [
            [1e-7, 0.0, 0.0],
            [0.0, 1e-7, 0.0],
            [0.0, 0.0, 1e-7],
        ],
    )


@dataclass
class Lidar3DConfig(SensorConfig):
    """Lidar 3D sensor configuration."""

    sensor_type_name: str = Lidar3D.__name__

    max_range: float = 100.0
    min_range: float = 0.0
    fov: float = field(
        default=360.0,
        metadata={"help": "Field of view in degrees."},
    )
    num_channels: int = field(
        default=4,
        metadata={"help": "Number of channels per point: x, y, z, intensity"},
    )
    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        metadata={"help": "Transformation matrix base link -> sensor."},
    )


@dataclass
class VrsGpsConfig(SensorConfig):
    sensor_type_name: str = VrsGps.__name__

    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        metadata={"help": "Transformation matrix base link -> sensor."},
    )


@dataclass
class UltraWideBandConfig(SensorConfig):
    sensor_type_name: str = UltraWideBand.__name__
