import gtsam
from gtsam.symbol_shorthand import B, L, N, P, V, X

from moduslam.frontend_manager.graph.base_vertices import (
    NotOptimizableVertex,
    OptimizableVertex,
)
from moduslam.types.aliases import Matrix3x3, Matrix4x4, Point3D, Vector3

identity_matrix = (
    (1.0, 0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0, 1.0),
)
zero_vector = (0.0, 0.0, 0.0)


class Pose(OptimizableVertex):
    """Pose vertex in Graph."""

    def __init__(self, index: int = 0, timestamp: int = 0, value: Matrix4x4 = identity_matrix):
        """
        Args:
            index: index of the vertex.
            timestamp: timestamp of the vertex.
            value: SE(3) pose.
        """
        super().__init__(index=index, timestamp=timestamp, value=value)
        self._backend_instance = gtsam.Pose3(value)

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return X(self.index)

    @property
    def backend_instance(self) -> gtsam.Pose3:
        """GTSAM pose."""
        return self._backend_instance

    @property
    def value(self) -> Matrix4x4:
        """Pose SE(3) matrix."""
        return self._value

    @property
    def position(self) -> Vector3:
        """Translation part of the pose: x, y, z."""
        return self.backend_instance.translation()

    @property
    def rotation(self) -> Matrix3x3:
        """Rotation part of the pose: SO(3) matrix."""
        return self.backend_instance.rotation().matrix()

    def update(self, value: gtsam.Values) -> None:
        """Updates the pose with the new value.

        Args:
            value: GTSAM values.
        """
        self._backend_instance = value.atPose3(self.backend_index)
        self._value = self.backend_instance.matrix()


class LinearVelocity(OptimizableVertex):
    """Linear velocity vertex in Graph."""

    def __init__(self, index: int = 0, timestamp: int = 0, value: Vector3 = zero_vector):
        super().__init__(index=index, timestamp=timestamp, value=value)

    @property
    def value(self) -> Vector3:
        """Linear velocity: Vx, Vy, Vz."""
        return self._value

    @property
    def backend_instance(self) -> Vector3:
        """Linear velocity: Vx, Vy, Vz.
        Identical to the value property, as GTSAM does not have a separate class for linear velocity.
        """
        return self.value

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return V(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the linear velocity with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atVector(self.backend_index)


class NavState(OptimizableVertex):
    """Navigation state vertex in Graph: pose & velocity."""

    def __init__(
        self,
        index: int = 0,
        timestamp: int = 0,
        value: tuple[Matrix4x4, Vector3] = (identity_matrix, zero_vector),
    ):
        super().__init__(index=index, timestamp=timestamp, value=value)
        pose, velocity = gtsam.Pose3(value[0]), value[1]
        self._backend_instance = gtsam.NavState(pose, velocity)

    @property
    def value(self) -> tuple[Matrix4x4, Vector3]:
        """NavState as SE(3) pose matrix and [Vx,Vy,Vz] vector."""
        return self._value

    @property
    def pose(self) -> Pose:
        """Pose part of the NavState: SE(3) matrix."""
        return self._value[0]

    @property
    def linear_velocity(self) -> Vector3:
        """Linear velocity part of the NavState: Vx, Vy, Vz."""
        return self._value[1]

    @property
    def backend_instance(self) -> gtsam.NavState:
        """GTSAM NavState instance."""
        return self._backend_instance

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return N(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the NavState with the new value.

        Args:
            value: GTSAM values.
        """
        self._backend_instance = value.atNavState(self.backend_index)
        self._value = self.backend_instance.pose().matrix(), self.backend_instance.velocity()


class Point(OptimizableVertex):
    def __init__(self, index: int = 0, timestamp: int = 0, value: Point3D = zero_vector):
        super().__init__(index=index, timestamp=timestamp, value=value)

    @property
    def value(self) -> Point3D:
        """Position of the point: x, y, z."""
        return self._value

    @property
    def backend_instance(self) -> Point3D:
        """Identical to the value property, as GTSAM does not have a separate class for
        point in 3D."""
        return self.value

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return P(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the point with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atPoint3(self.backend_index)


class ImuBias(OptimizableVertex):
    """Imu bias in Graph."""

    def __init__(
        self,
        index: int = 0,
        timestamp: int = 0,
        value: tuple[Vector3, Vector3] = (zero_vector, zero_vector),
    ):
        """
        Args:
            index: index of the vertex.
            timestamp: timestamp of the vertex.
            value: accelerometer bias, gyroscope bias.
        """
        super().__init__(index=index, timestamp=timestamp, value=value)
        self._backend_instance = gtsam.imuBias.ConstantBias(value[0], value[1])

    @property
    def value(self) -> tuple[Vector3, Vector3]:
        """Accelerometer and gyroscope biases: (Bx, By, Bz), (Bx, By, Bz)."""
        return self._value

    @property
    def accelerometer_bias(self) -> Vector3:
        """Accelerometer bias: Bx, By, Bz."""
        return self._value[0]

    @property
    def gyroscope_bias(self) -> Vector3:
        """Gyroscope bias: Bx, By, Bz."""
        return self._value[1]

    @property
    def backend_instance(self) -> gtsam.imuBias.ConstantBias:
        """GTSAM instance."""
        return self._backend_instance

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return B(self.index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the Imu bias with the new value.

        Args:
            value: GTSAM values.
        """
        self._backend_instance = value.atConstantBias(self.backend_index)
        self._value = self.backend_instance.accelerometer(), self.backend_instance.gyroscope()


class CameraPose(Pose):
    """The pose where an image has been taken."""


class LidarPose(Pose):
    """The pose where a point-cloud has been registered."""


class PoseLandmark(Pose):
    """Base landmark in the Graph."""

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return L(self.index)


class Feature3D(NotOptimizableVertex):
    """Non-optimizable point in 3D."""

    def __init__(self, index: int = 0, timestamp: int = 0, value: Point3D = zero_vector):
        super().__init__(index=index, timestamp=timestamp, value=value)

    @property
    def value(self) -> Point3D:
        """Position of the feature: x, y, z."""
        return self._value

    def update(self, value: Point3D) -> None:
        """Updates the feature with the new value.

        Args:
            value: New value of the feature.
        """
        self._value = value
