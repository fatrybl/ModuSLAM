import gtsam

from phd.measurements.processed_measurements import (
    ContinuousMeasurement,
    Imu,
    Measurement,
)
from phd.measurements.processed_measurements import PoseLandmark as DetectedLandmark
from phd.moduslam.frontend_manager.main_graph.edges.base import (
    BinaryEdge,
    Edge,
    RadialEdge,
    UnaryEdge,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    Feature3D,
    ImuBias,
    LinearVelocity,
    Pose,
    PoseLandmark,
)


class PoseToLandmark(BinaryEdge[Pose, PoseLandmark]):
    """Connects a Pose with a Landmark Pose."""

    def __init__(
        self,
        pose: Pose,
        landmark: PoseLandmark,
        measurement: DetectedLandmark,
        factor: gtsam.BetweenFactorPose3,
        noise_model: gtsam.noiseModel.Base,
    ):

        super().__init__(pose, landmark, measurement, factor, noise_model)


class SmartVisualFeature(RadialEdge[Feature3D, Pose]):
    """Edge for SmartProjectionPose3Factor: https://dellaert.github.io/files/Carlone14icra.pdf"""

    def __init__(
        self,
        feature: Feature3D,
        poses: list[Pose],
        measurements: list[Measurement],
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            feature: 3D feature.

            poses: camera poses.

            measurements: a measurement with the distance to the visual feature.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(feature, poses, measurements, factor, noise_model)

    @property
    def factor(self) -> gtsam.SmartProjectionPose3Factor:
        """GTSAM factor."""
        return self._factor

    @property
    def central_vertex(self) -> Feature3D:
        """Central vertex of the edge."""
        return self._center

    @property
    def radial_vertices(self) -> list[Pose]:
        """Radial vertices of the edge."""
        return self._radials

    @property
    def measurements(self) -> list[Measurement]:
        """Measurements which formed the edge."""
        return self._measurements


class ImuOdometry(Edge):
    """Edge for Imu pre-integrated odometry."""

    def __init__(
        self,
        pose_i: Pose,
        velocity_i: LinearVelocity,
        bias_i: ImuBias,
        pose_j: Pose,
        velocity_j: LinearVelocity,
        bias_j: ImuBias,
        measurement: ContinuousMeasurement[Imu],
        factor: gtsam.ImuFactor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:

            measurement: measurements which formed the edge.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(factor, noise_model)
        self._pose_i = pose_i
        self._velocity_i = velocity_i
        self._bias_i = bias_i
        self._pose_j = pose_j
        self._velocity_j = velocity_j
        self._bias_j = bias_j
        self._vertices = (pose_i, velocity_i, bias_i, pose_j, velocity_j, bias_j)
        self._measurement = measurement

    @property
    def vertices(self) -> tuple[Pose, LinearVelocity, ImuBias, Pose, LinearVelocity, ImuBias]:
        """Vertices of the edge."""
        return self._vertices

    @property
    def measurement(self) -> ContinuousMeasurement[Imu]:
        """Measurement which formed the edge."""
        return self._measurement


class PoseOdometry(BinaryEdge[Pose, Pose]):
    """Edge for a Pose-based odometry."""

    def __init__(
        self,
        vertex1: Pose,
        vertex2: Pose,
        measurement: Measurement,
        factor: gtsam.BetweenFactorPose3,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        super().__init__(vertex1, vertex2, measurement, factor, noise_model)


class VisualOdometry(BinaryEdge):
    """Edge for Stereo Camera odometry."""


class PriorPose(UnaryEdge):
    """Edge for prior pose."""


class PriorVelocity(UnaryEdge):
    """Edge for prior velocity."""


class PriorNavState(UnaryEdge):
    """Edge for prior nav state."""


class GpsPosition(UnaryEdge):
    """Edge for GPS position."""
