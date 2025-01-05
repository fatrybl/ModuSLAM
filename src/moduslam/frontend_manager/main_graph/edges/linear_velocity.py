import gtsam
from gtsam.noiseModel import Base

from src.measurement_storage.measurements.linear_velocity import (
    Velocity as VelocityMeasurement,
)
from src.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity as VelocityVertex,
)


class LinearVelocity(UnaryEdge):
    """Edge for prior velocity."""

    def __init__(
        self,
        velocity: VelocityVertex,
        measurement: VelocityMeasurement,
        noise_model: Base,
    ):
        super().__init__()
        self._measurement = measurement
        self._velocity = velocity
        self._factor = gtsam.PriorFactorVector(
            velocity.backend_index, measurement.velocity, noise_model
        )

    @property
    def factor(self) -> gtsam.PriorFactorVector:
        """gtsam.PriorFactorVector."""
        return self._factor

    @property
    def vertex(self) -> VelocityVertex:
        return self._velocity

    @property
    def vertices(self) -> tuple[VelocityVertex]:
        return (self._velocity,)

    @property
    def measurement(self) -> VelocityMeasurement:
        return self._measurement
