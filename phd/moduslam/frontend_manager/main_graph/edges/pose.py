import gtsam
from gtsam.noiseModel import Base

from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.base import UnaryEdge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex


class Pose(UnaryEdge):
    """Edge for prior pose."""

    def __init__(self, pose: PoseVertex, measurement: PoseMeasurement, noise_model: Base):
        """
        Args:
            pose: a Pose vertex.

            measurement: a measurement with SE(3) transformation matrix.

            noise_model: a GTSAM noise model.
        """

        super().__init__()
        self._vertex = pose
        self._measurement = measurement
        tf = gtsam.Pose3(measurement.pose)
        self._factor = gtsam.PriorFactorPose3(pose.backend_index, tf, noise_model)

    @property
    def factor(self) -> gtsam.BetweenFactorPose3:
        """gtsam.BetweenFactorPose3."""
        return self._factor

    @property
    def vertex(self) -> PoseVertex:
        return self._vertex

    @property
    def vertices(self) -> tuple[PoseVertex]:
        return (self._vertex,)

    @property
    def measurement(self) -> PoseMeasurement:
        return self._measurement
