from dataclasses import dataclass, field

from src.moduslam.sensors_factory.sensors import (
    Imu,
    Lidar3D,
    Sensor,
    StereoCamera,
    VrsGps,
)


@dataclass
class SensorConfig:
    """Base sensor configuration."""

    name: str
    type_name: str = Sensor.__name__


@dataclass
class StereoCameraConfig(SensorConfig):

    type_name: str = StereoCamera.__name__

    camera_matrix_left: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    camera_matrix_right: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    distortion_coefficients_left: list[float] = field(
        default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0]
    )

    distortion_coefficients_right: list[float] = field(
        default_factory=lambda: [0.0, 0.0, 0.0, 0.0, 0.0]
    )

    rectification_matrix_left: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    rectification_matrix_right: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )

    projection_matrix_left: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

    projection_matrix_right: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )

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

    distortion_model_left: str = "plumb_bob"
    distortion_model_right: str = "plumb_bob"


@dataclass
class ImuConfig(SensorConfig):
    """IMU sensor configuration."""

    type_name: str = Imu.__name__

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

    type_name: str = Lidar3D.__name__

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

    type_name = VrsGps.__name__

    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        metadata={"help": "Transformation matrix base link -> sensor."},
    )
