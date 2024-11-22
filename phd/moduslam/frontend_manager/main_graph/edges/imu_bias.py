import gtsam

from phd.measurements.processed_measurements import ImuBias as ImuBiasMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias as BiasVertex,
)


class ImuBias(UnaryEdge):
    """Edge for constant IMU bias."""

    def __init__(
        self,
        imu_bias: BiasVertex,
        measurement: ImuBiasMeasurement,
    ):
        super().__init__()
        self._vertex = imu_bias
        self._measurement = measurement
        accel = measurement.linear_acceleration_bias
        gyro = measurement.angular_velocity_bias
        self._factor = gtsam.imuBias.ConstantBias(accel, gyro)

    @property
    def factor(self) -> gtsam.imuBias.ConstantBias:
        """gtsam.imuBias.ConstantBias."""
        return self._factor

    @property
    def vertex(self) -> BiasVertex:
        return self._vertex

    @property
    def measurement(self) -> ImuBiasMeasurement:
        return self._measurement

    @property
    def vertices(self) -> tuple[BiasVertex]:
        return (self._vertex,)
