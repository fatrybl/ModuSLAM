from gtsam import ImuFactor, PreintegratedImuMeasurements

from phd.measurement_storage.measurements.imu import ContinuousImu
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)


class ImuOdometry(Edge):
    """Pre-integrated IMU odometry edge."""

    def __init__(
        self,
        pose_i: Pose,
        velocity_i: LinearVelocity,
        bias_i: ImuBias,
        pose_j: Pose,
        velocity_j: LinearVelocity,
        measurement: ContinuousImu,
        pim: PreintegratedImuMeasurements,
    ) -> None:
        """
        Args:
            pose_i: initial pose.

            velocity_i: initial velocity.

            bias_i: initial IMU bias.

            pose_j: final pose.

            velocity_j: final velocity.

            measurement: continuous IMU measurement.

            pim: a GTSAM pre-integrated IMU measurements.
        """
        super().__init__()
        self._pose_i = pose_i
        self._velocity_i = velocity_i
        self._bias_i = bias_i
        self._pose_j = pose_j
        self._velocity_j = velocity_j
        self._vertices = (pose_i, velocity_i, bias_i, pose_j, velocity_j)
        self._measurement = measurement
        self._factor = self._create_factor(self._vertices, pim)

    @property
    def factor(self) -> ImuFactor:
        """gtsam.ImuFactor."""
        return self._factor

    @property
    def vertices(self) -> tuple[Pose, LinearVelocity, ImuBias, Pose, LinearVelocity]:
        """Vertices of the edge."""
        return self._vertices

    @property
    def measurement(self) -> ContinuousImu:
        """Measurement which formed the edge."""
        return self._measurement

    @property
    def pose_i(self) -> Pose:
        """Start pose."""
        return self._pose_i

    @property
    def pose_j(self) -> Pose:
        """Stop pose."""
        return self._pose_j

    @property
    def velocity_i(self) -> LinearVelocity:
        """Start velocity."""
        return self._velocity_i

    @property
    def velocity_j(self) -> LinearVelocity:
        """Stop velocity."""
        return self._velocity_j

    @property
    def bias_i(self) -> ImuBias:
        """Start IMU bias."""
        return self._bias_i

    @staticmethod
    def _create_factor(
        vertices: tuple[Pose, LinearVelocity, ImuBias, Pose, LinearVelocity],
        pim: PreintegratedImuMeasurements,
    ) -> ImuFactor:
        pi = vertices[0].backend_index
        vi = vertices[1].backend_index
        bi = vertices[2].backend_index
        pj = vertices[3].backend_index
        vj = vertices[4].backend_index
        return ImuFactor(pi, vi, pj, vj, bi, pim)
