from collections.abc import Sequence

import gtsam

from moduslam.frontend_manager.graph.base_edges import (
    BinaryEdge,
    MultiEdge,
    RadialEdge,
    UnaryEdge,
)
from moduslam.frontend_manager.graph.custom_vertices import CameraPose, Feature3D
from moduslam.frontend_manager.measurement_storage import Measurement


class SmartVisualFeature(RadialEdge):
    """Edge for SmartProjectionPose3Factor: https://dellaert.github.io/files/Carlone14icra.pdf"""

    def __init__(
        self,
        feature: Feature3D,
        poses: Sequence[CameraPose],
        measurements: Sequence[Measurement],
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
        self._radials: list[CameraPose] = list(poses)
        self._measurements: list[Measurement] = list(measurements)

    @property
    def factor(self) -> gtsam.SmartProjectionPose3Factor:
        """GTSAM factor."""
        return self._factor

    @property
    def central_vertex(self) -> Feature3D:
        """Central vertex of the edge."""
        return self._center

    @property
    def radial_vertices(self) -> list[CameraPose]:
        """Radial vertices of the edge."""
        return self._radials

    @property
    def vertices(self) -> tuple[Feature3D | CameraPose, ...]:
        """Vertices of the edge."""
        return self._center, *self._radials

    @property
    def measurements(self) -> list[Measurement]:
        """Measurements which formed the edge."""
        return self._measurements


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
