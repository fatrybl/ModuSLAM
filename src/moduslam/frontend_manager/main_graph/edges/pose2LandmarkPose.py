import gtsam
from gtsam.noiseModel import Base

from src.measurement_storage.measurements.with_raw_elements import (
    PoseLandmark as DetectedLandmark,
)
from src.moduslam.frontend_manager.main_graph.edges.base import BinaryEdge
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    Pose,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    PoseLandmark as LandmarkVertex,
)


class PoseToLandmark(BinaryEdge):
    """Connects a Pose with a Landmark Pose."""

    def __init__(
        self, pose: Pose, landmark: LandmarkVertex, measurement: DetectedLandmark, noise_model: Base
    ):
        """
        Args:
            pose: a Pose vertex.

            landmark: a Landmark vertex.

            measurement: a measurement with the landmark pose.

            noise_model: a GTSAM noise model.
        """

        super().__init__()
        self._vertex1 = pose
        self._vertex2 = landmark
        self._measurement = measurement
        self._factor = gtsam.BetweenFactorPose3(
            pose.backend_index, landmark.backend_index, measurement.transformation, noise_model
        )

    @property
    def factor(self) -> gtsam.BetweenFactorPose3:
        """gtsam.BetweenFactorPose3."""
        return self._factor

    @property
    def vertex1(self) -> Pose:
        return self._vertex1

    @property
    def vertex2(self) -> LandmarkVertex:
        return self._vertex2

    @property
    def vertices(self) -> tuple[Pose, LandmarkVertex]:
        return self._vertex1, self._vertex2

    @property
    def measurement(self) -> DetectedLandmark:
        return self._measurement
