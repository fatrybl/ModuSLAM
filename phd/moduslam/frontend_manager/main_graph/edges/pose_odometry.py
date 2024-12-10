import gtsam
from gtsam.noiseModel import Base

from phd.measurement_storage.measurements.pose_odometry import (
    Odometry as OdometryMeasurement,
)
from phd.moduslam.frontend_manager.main_graph.edges.base import BinaryEdge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose


class PoseOdometry(BinaryEdge):
    """Edge for a Pose-based odometry."""

    def __init__(
        self, pose_i: Pose, pose_j: Pose, measurement: OdometryMeasurement, noise_model: Base
    ):
        """
        Args:
            pose_i: i-th Pose vertex.

            pose_j: j-th Pose vertex.

            measurement: a measurement with SE(3) transformation matrix.

            noise_model: a GTSAM noise model.
        """

        super().__init__()
        self._vertex1 = pose_i
        self._vertex2 = pose_j
        self._measurement = measurement
        tf = gtsam.Pose3(measurement.pose)
        self._factor = gtsam.BetweenFactorPose3(
            pose_i.backend_index, pose_j.backend_index, tf, noise_model
        )

    @property
    def factor(self) -> gtsam.BetweenFactorPose3:
        """gtsam.BetweenFactorPose3."""
        return self._factor

    @property
    def vertex1(self) -> Pose:
        return self._vertex1

    @property
    def vertex2(self) -> Pose:
        return self._vertex2

    @property
    def vertices(self) -> tuple[Pose, Pose]:
        return self._vertex1, self._vertex2

    @property
    def measurement(self) -> OdometryMeasurement:
        return self._measurement
