import gtsam
from gtsam.symbol_shorthand import B, L, N, P, V, X

from slam.frontend_manager.graph.base_vertices import (
    NotOptimizableVertex,
    OptimizableVertex,
)
from slam.utils.auxiliary_methods import create_vector_3
from slam.utils.numpy_types import Matrix3x3, Matrix4x4, Vector3


class Pose(OptimizableVertex):
    """Pose vertex in Graph."""

    def __init__(self):
        super().__init__()
        self._value = gtsam.Pose3()

    @property
    def position(self) -> Vector3:
        """Translation part of the pose: x, y, z."""
        return self._value.translation()

    @property
    def rotation(self) -> Matrix3x3:
        """Rotation part of the pose: SO(3) matrix."""
        return self._value.rotation().matrix()

    @property
    def pose(self) -> Matrix4x4:
        """Pose as SE(3) matrix."""
        return self._value.matrix()

    @property
    def gtsam_index(self) -> int:
        """GTSAM instance index."""
        return X(self.index)

    @property
    def gtsam_instance(self) -> gtsam.Pose3:
        """GTSAM pose."""
        return self._value

    def update(self, value: gtsam.Values) -> None:
        """Updates the pose with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atPose3(self.gtsam_index)


class Velocity(OptimizableVertex):
    """Linear velocity vertex in Graph."""

    def __init__(self):
        super().__init__()
        self._value = create_vector_3(0.0, 0.0, 0.0)

    @property
    def linear_velocity(self) -> Vector3:
        """Linear velocity: Vx, Vy, Vz."""
        return self._value

    @property
    def gtsam_instance(self) -> Vector3:
        """Linear velocity: Vx, Vy, Vz.
        Identical to the linear_velocity property.
        """
        return self._value

    @property
    def gtsam_index(self) -> int:
        """GTSAM instance index."""
        return V(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the linear velocity with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atVector(self.gtsam_index)


class NavState(OptimizableVertex):
    """Navigation state vertex in Graph: pose & velocity."""

    def __init__(self):
        super().__init__()
        self._value: gtsam.NavState = gtsam.NavState()

    @property
    def pose(self) -> Pose:
        """Pose part of the NavState: SE(3) matrix."""
        return self._value.pose()

    @property
    def velocity(self) -> Vector3:
        """Linear velocity part of the NavState: Vx, Vy, Vz."""
        return self._value.velocity()

    @property
    def gtsam_instance(self) -> gtsam.NavState:
        """GTSAM NavState instance."""
        return self._value

    @property
    def gtsam_index(self) -> int:
        """GTSAM instance index."""
        return N(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the NavState with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atNavState(self.gtsam_index)


class Point(OptimizableVertex):
    def __init__(self):
        super().__init__()
        self._value: Vector3 = create_vector_3(0, 0, 0)

    @property
    def position(self) -> Vector3:
        """Position of the point: x, y, z."""
        return self._value

    @property
    def gtsam_instance(self) -> Vector3:
        """GTSAM instance of the point."""
        return self._value

    @property
    def gtsam_index(self) -> int:
        """GTSAM instance index."""
        return P(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the point with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atPoint3(self.gtsam_index)


class ImuBias(OptimizableVertex):
    """Imu bias in Graph."""

    def __init__(self):
        super().__init__()
        self._value: gtsam.imuBias.ConstantBias = gtsam.imuBias.ConstantBias()

    @property
    def accelerometer_bias(self) -> Vector3:
        """Accelerometer bias: Bx, By, Bz."""
        return self._value.accelerometer()

    @property
    def gyroscope_bias(self) -> Vector3:
        """Gyroscope bias: Bx, By, Bz."""
        return self._value.gyroscope()

    @property
    def gtsam_instance(self) -> gtsam.imuBias.ConstantBias:
        """GTSAM instance."""
        return self._value

    @property
    def gtsam_index(self) -> int:
        """GTSAM instance index."""
        return B(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the Imu bias with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atConstantBias(self.gtsam_index)


class CameraPose(Pose):
    """The pose where an image has been taken."""


class LidarPose(Pose):
    """The pose where a point-cloud has been registered."""


class PoseLandmark(Pose):
    """Base landmark in the Graph."""

    @property
    def gtsam_index(self) -> int:
        """GTSAM instance index."""
        return L(self.index)


class Feature(NotOptimizableVertex):
    """Non-optimizable point in 3D."""

    def __init__(self):
        super().__init__()
        self._value: Vector3 = create_vector_3(0.0, 0.0, 0.0)

    @property
    def position(self) -> Vector3:
        """Position of the feature: x, y, z."""
        return self._value

    def update(self, value: Vector3) -> None:
        """Updates the feature with the new value.

        Args:
            value: New value of the feature.
        """
        self._value = value


class CameraFeature(Feature):
    """Feature in the Camera Frame."""
