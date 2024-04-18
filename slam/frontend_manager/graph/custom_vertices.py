from typing import TypeAlias

import gtsam
from gtsam.symbol_shorthand import B, L, N, P, V, X

from slam.frontend_manager.graph.base_vertices import OptimizableVertex, Vertex
from slam.utils.auxiliary_methods import vector_3
from slam.utils.numpy_types import Matrix3x3, Matrix4x4, Vector3

GtsamVertex: TypeAlias = gtsam.Rot3 | gtsam.Pose3 | gtsam.NavState | gtsam.imuBias.ConstantBias


class Pose(OptimizableVertex):
    """Pose vertex in Graph."""

    def __init__(self):
        super().__init__()
        self._value = gtsam.Pose3()

    @property
    def position(self) -> Vector3:
        """
        Translation part of the pose: x, y, z.
        Returns:
            position (Vector3).
        """
        return self._value.translation()

    @property
    def rotation(self) -> Matrix3x3:
        """
        Rotation part of the pose: SO(3) matrix.
        Returns:
            rotation (Matrix3x3).
        """
        return self._value.rotation().matrix()

    @property
    def pose(self) -> Matrix4x4:
        """Pose as SE(3) matrix.

        Returns:
            pose (Matrix4x4).
        """
        return self._value.matrix()

    @property
    def gtsam_index(self) -> int:
        """Index of the variable in the GTSAM Values.

        Returns:
            (int): index.
        """
        return X(self.index)

    @property
    def gtsam_value(self) -> gtsam.Pose3:
        """GTSAM value of the vertex.

        Returns:
            value (gtsam.Pose3).
        """
        return self._value

    def update(self, values: gtsam.Values) -> None:
        self._value = values.atPose3(self.gtsam_index)


class Velocity(OptimizableVertex):
    """Linear velocity vertex in Graph."""

    def __init__(self):
        super().__init__()
        self._value = vector_3(0.0, 0.0, 0.0)

    @property
    def linear_velocity(self) -> Vector3:
        """
        Linear velocity: Vx, Vy, Vz.

        Returns:
            linear_velocity (Vector3).
        """
        return self._value

    @property
    def gtsam_value(self) -> Vector3:
        return self._value

    @property
    def gtsam_index(self) -> int:
        return V(self.index)

    def update(self, values: gtsam.Values) -> None:
        self._value = values.atVector(self.gtsam_index)


class NavState(OptimizableVertex):
    """Navigation state vertex in the Graph: pose and velocity."""

    def __init__(self):
        super().__init__()
        self._value: gtsam.NavState = gtsam.NavState()

    @property
    def pose(self) -> Pose:
        """
        Pose part of the NavState: SE(3) matrix.

        Returns:
            pose (Matrix4x4).
        """
        return self._value.pose()

    @property
    def velocity(self) -> Vector3:
        """
        Linear velocity part of the NavState: Vx, Vy, Vz.

        Returns:
            velocity (Vector3).
        """
        return self._value.velocity()

    @property
    def gtsam_value(self) -> gtsam.NavState:
        return self._value

    @property
    def gtsam_index(self) -> int:
        return N(self.index)

    def update(self, values: gtsam.Values) -> None:
        self._value = values.atNavState(self.gtsam_index)


class Point(OptimizableVertex):
    def __init__(self):
        super().__init__()
        self._value: Vector3 = vector_3(0, 0, 0)

    @property
    def position(self) -> Vector3:
        """
        Position of the point: x, y, z.

        Returns:
            position (Vector3).
        """
        return self._value

    @property
    def gtsam_value(self) -> Vector3:
        return self._value

    @property
    def gtsam_index(self) -> int:
        return P(self.index)

    def update(self, values: gtsam.Values) -> None:
        self._value = values.atPoint3(self.gtsam_index)


class ImuBias(OptimizableVertex):
    """Imu bias in the Graph."""

    def __init__(self):
        super().__init__()
        self._value: gtsam.imuBias.ConstantBias = gtsam.imuBias.ConstantBias()

    @property
    def accelerometer_bias(self) -> Vector3:
        """
        Accelerometer bias: Bx, By, Bz.

        Returns:
            accelerometer_bias (Vector3).
        """
        return self._value.accelerometer()

    @property
    def gyroscope_bias(self) -> Vector3:
        """
        Gyroscope bias: Bx, By, Bz.

        Returns:
            gyroscope_bias (Vector3).
        """
        return self._value.gyroscope()

    @property
    def gtsam_value(self) -> gtsam.imuBias.ConstantBias:
        return self._value

    @property
    def gtsam_index(self) -> int:
        return B(self.index)

    def update(self, values: gtsam.Values) -> None:
        self._value = values.atConstantBias(self.gtsam_index)


class CameraPose(Pose):
    """The pose where an image has been taken."""


class LidarPose(Pose):
    """The pose where a point-cloud has been registered."""


class PoseLandmark(Pose):
    """Base landmark in the Graph."""

    @property
    def gtsam_index(self) -> int:
        return L(self.index)


class Feature(Vertex):
    """Non-optimizable point in 3D."""

    def __init__(self):
        super().__init__()
        self._value: Vector3 = vector_3(0.0, 0.0, 0.0)

    @property
    def position(self) -> Vector3:
        """
        Position of the feature: x, y, z.

        Returns:
            position (Vector3).
        """
        return self._value

    def update(self, values: Vector3) -> None:
        self._value = values


class CameraFeature(Feature):
    """Feature in the Camera Frame."""
