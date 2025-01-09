"""A table with measurements` type names and the corresponding methods to create a
measurement."""

from collections.abc import Callable

from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.imu_bias import Bias
from src.measurement_storage.measurements.linear_velocity import Velocity
from src.measurement_storage.measurements.pose import Pose
from src.measurement_storage.measurements.position import Position
from src.moduslam.frontend_manager.graph_initializer.utils import (
    create_imu_bias,
    create_linear_velocity,
    create_pose,
    create_position,
)

type_method_table: dict[str, Callable[..., Measurement]] = {
    Position.__name__: create_position,
    Pose.__name__: create_pose,
    Velocity.__name__: create_linear_velocity,
    Bias.__name__: create_imu_bias,
}
