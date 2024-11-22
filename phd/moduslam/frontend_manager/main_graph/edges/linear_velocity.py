import gtsam
from gtsam.noiseModel import Base

from phd.measurements.processed_measurements import (
    LinearVelocity as LinearVelocityMeasurement,
)
from phd.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity as VelocityVertex,
)


class LinearVelocity(UnaryEdge):
    """Edge for prior velocity."""

    def __init__(
        self,
        velocity: VelocityVertex,
        measurement: LinearVelocityMeasurement,
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
    def measurement(self) -> LinearVelocityMeasurement:
        return self._measurement
