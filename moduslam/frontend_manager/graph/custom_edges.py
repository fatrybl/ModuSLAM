import gtsam

from moduslam.frontend_manager.graph.base_edges import BinaryEdge, MultiEdge, UnaryEdge
from moduslam.frontend_manager.graph.base_vertices import (
    NotOptimizableVertex,
    OptimizableVertex,
)
from moduslam.frontend_manager.measurement_storage import Measurement


class SmartVisualFeature(BinaryEdge):
    """Edge for Smart Factor in the Graph: https://dellaert.github.io/files/Carlone14icra.pdf"""

    def __init__(
        self,
        base_vertex: OptimizableVertex,
        support_vertex: NotOptimizableVertex,
        measurement: Measurement,
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            base_vertex: main vertex.

            support_vertex: support vertices

            measurement: a measurement with the distance to the visual feature.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(base_vertex, support_vertex, (measurement,), factor, noise_model)


class ImuOdometry(MultiEdge):
    """Edge for Imu pre-integrated odometry."""


class LidarOdometry(BinaryEdge):
    """Edge for Lidar odometry."""


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
