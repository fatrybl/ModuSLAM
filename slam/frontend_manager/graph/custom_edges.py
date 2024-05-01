import gtsam

from slam.frontend_manager.graph.base_edges import (
    BinaryEdge,
    CalibrationEdge,
    MultiEdge,
    UnaryEdge,
)
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.measurement_storage import Measurement


class SmartFactor(CalibrationEdge):
    """Edge for Smart Factor in the Graph: https://dellaert.github.io/files/Carlone14icra.pdf"""

    def __init__(
        self,
        vertex: GraphVertex,
        support_vertices: set[GraphVertex],
        measurements: tuple[Measurement, ...],
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            vertex: target vertex.

            support_vertices: support vertices

            measurements: measurements to be used in the factor.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(measurements, vertex, support_vertices, factor, noise_model)

    @property
    def all_vertices(self) -> set[GraphVertex]:
        """Vertices of the edge."""
        return {self.vertex}.union(self.vertices)


class SmartStereoFeature(SmartFactor):
    """Edge for smart Stereo Camera features."""

    def __init__(
        self,
        vertex: GraphVertex,
        support_vertices: set[GraphVertex],
        measurements: tuple[Measurement, ...],
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """

        Args:
            vertex: target vertex (camera pose).

            support_vertices: camera feature vertices.

            measurements: from pose to features.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(vertex, support_vertices, measurements, factor, noise_model)

        self.K: gtsam.Cal3_S2 = gtsam.Cal3_S2()
        self.params: gtsam.SmartProjectionParams = gtsam.SmartProjectionParams()
        self.sensor_body: gtsam.Pose3 = gtsam.Pose3()


class ImuOdometry(MultiEdge):
    """Edge for Imu pre-integrated odometry."""


class LidarOdometry(BinaryEdge):
    """Edge for Lidar odometry."""


class StereoCameraOdometry(BinaryEdge):
    """Edge for Stereo Camera odometry."""


class PriorPose(UnaryEdge):
    """Edge for prior pose."""


class PriorVelocity(UnaryEdge):
    """Edge for prior velocity."""


class PriorNavState(UnaryEdge):
    """Edge for prior nav state."""
