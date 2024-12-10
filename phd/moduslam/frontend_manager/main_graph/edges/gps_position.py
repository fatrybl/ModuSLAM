import gtsam
from gtsam.gtsam.noiseModel import Base

from phd.measurement_storage.measurements.gps import Gps
from phd.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose


class GpsPosition(UnaryEdge):
    """Edge for GPS position."""

    def __init__(self, pose: Pose, measurement: Gps, noise_model: Base):
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
    def measurement(self) -> Gps:
        return self._measurement

    @property
    def vertices(self) -> tuple[Pose]:
        return (self._pose,)
