import gtsam
from gtsam.gtsam.noiseModel import Base

from src.measurement_storage.measurements.position import Position
from src.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose


class GpsPosition(UnaryEdge):
    """Edge for GPS position."""

    def __init__(self, pose: Pose, measurement: Position, noise_model: Base):
        """
        Args:
            pose: a pose vertex.

            measurement: a GPS measurement.

            noise_model: a GTSAM noise model.
        """
        super().__init__()
        self._pose = pose
        self._measurement = measurement
        self._factor = gtsam.GPSFactor(pose.backend_index, measurement.position, noise_model)

    @property
    def factor(self) -> gtsam.GPSFactor:
        """gtsam.GPSFactor."""
        return self._factor

    @property
    def vertex(self) -> Pose:
        return self._pose

    @property
    def measurement(self) -> Position:
        return self._measurement

    @property
    def vertices(self) -> tuple[Pose]:
        return (self._pose,)
