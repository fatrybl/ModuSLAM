"""A table with vertices types names and the corresponding methods to create a
measurement."""

from collections.abc import Callable

from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.graph_initializer.utils import (
    create_imu_bias,
    create_linear_velocity,
    create_pose,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias as ImuBiasVertex,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity as VelocityVertex,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex

type_method_table: dict[str, Callable[..., Measurement]] = {
    PoseVertex.__name__: create_pose,
    VelocityVertex.__name__: create_linear_velocity,
    ImuBiasVertex.__name__: create_imu_bias,
}
