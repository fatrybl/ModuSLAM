from collections.abc import Sequence

import gtsam

from moduslam.frontend_manager.graph.base_edges import (
    BinaryEdge,
    MultiEdge,
    RadialEdge,
    UnaryEdge,
)
from moduslam.frontend_manager.graph.base_vertices import OptimizableVertex
from moduslam.frontend_manager.graph.custom_vertices import Feature3D
from moduslam.frontend_manager.measurement_storage import Measurement


class SmartVisualFeature(RadialEdge):
    """Edge for SmartProjectionPose3Factor: https://dellaert.github.io/files/Carlone14icra.pdf"""

    def __init__(
        self,
        pose: OptimizableVertex,
        features: Sequence[Feature3D],
        measurements: Sequence[Measurement],
        factor: gtsam.SmartProjectionPose3Factor,
        noise_model: gtsam.noiseModel.Base,
    ) -> None:
        """
        Args:
            pose: optimizable pose.

            features: non-optimizable 3D points.

            measurements: a measurement with the distance to the visual feature.

            factor: GTSAM factor.

            noise_model: GTSAM noise model of the factor.
        """
        super().__init__(pose, features, measurements, factor, noise_model)


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
