import gtsam
import numpy as np
from gtsam.noiseModel import Base

from phd.measurement_storage.measurements.imu_bias import Bias as BiasMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias as BiasVertex,
)


class ImuBias(UnaryEdge):
    """Edge for constant IMU bias."""

    def __init__(self, imu_bias: BiasVertex, measurement: BiasMeasurement, noise_model: Base):
        super().__init__()
        self._vertex = imu_bias
        self._measurement = measurement
        accel = np.array(measurement.linear_acceleration_bias)
        gyro = np.array(measurement.angular_velocity_bias)
        index = imu_bias.backend_index
        bias = gtsam.imuBias.ConstantBias(accel, gyro)
        self._factor = gtsam.PriorFactorConstantBias(index, bias, noise_model)

    @property
    def factor(self) -> gtsam.PriorFactorConstantBias:
        """gtsam.imuBias.ConstantBias."""
        return self._factor

    @property
    def vertex(self) -> BiasVertex:
        return self._vertex

    @property
    def measurement(self) -> BiasMeasurement:
        return self._measurement

    @property
    def vertices(self) -> tuple[BiasVertex]:
        return (self._vertex,)
