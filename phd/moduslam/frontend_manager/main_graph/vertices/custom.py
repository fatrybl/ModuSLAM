import gtsam
from gtsam.symbol_shorthand import B, L, N, P, V, X

from phd.moduslam.custom_types.aliases import Matrix3x3, Matrix4x4, Vector3
from phd.moduslam.frontend_manager.main_graph.vertices.base import (
    NonOptimizableVertex,
    OptimizableVertex,
)
from phd.utils.auxiliary_objects import identity4x4, zero_vector3


class Pose(OptimizableVertex):
    """Pose vertex in Graph."""

    def __init__(self, index: int, value: Matrix4x4 = identity4x4):
        """
        Args:
            index: index of the vertex.

            value: SE(3) pose.
        """
        super().__init__(index, value)
        self._backend_instance = gtsam.Pose3(value)

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return X(self._index)

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
        return self._backend_instance.translation()

    @property
    def rotation(self) -> Matrix3x3:
        """Rotation part of the pose: SO(3) matrix."""
        return self._backend_instance.rotation().matrix()

    def update(self, value: gtsam.Values) -> None:
        """Updates the pose with the new value.

        Args:
            value: GTSAM values.
        """
        self._backend_instance = value.atPose3(self.backend_index)
        self._value = self._backend_instance.matrix()


class PoseLandmark(Pose):
    """Landmark with the 3D Pose."""

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return L(self._index)


class LinearVelocity(OptimizableVertex):
    """Linear velocity vertex in Graph."""

    def __init__(self, index: int, value: Vector3 = zero_vector3):
        """
        Args:
            index: index of the vertex.

            value: x,y,z velocity vector.
        """
        super().__init__(index, value)

    @property
    def value(self) -> Vector3:
        """Linear velocity: Vx, Vy, Vz."""
        return self._value

    @property
    def backend_instance(self) -> Vector3:
        """Linear velocity: Vx, Vy, Vz.
        Identical to the value property, as GTSAM does not have a separate class for linear velocity.
        """
        return self._value

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return V(self._index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the linear velocity with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atVector(self.backend_index)


class NavState(OptimizableVertex):
    """Navigation state vertex in Graph: pose & velocity."""

    def __init__(self, index: int, value: tuple[Matrix4x4, Vector3] = (identity4x4, zero_vector3)):
        """
        Args:
            index: index of the vertex.

            value: SE(3) pose, x,y,z velocity vector.
        """
        super().__init__(index, value)
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
        return N(self._index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the NavState with the new value.

        Args:
            value: GTSAM values.
        """
        self._backend_instance = value.atNavState(self.backend_index)
        self._value = (
            self._backend_instance.transformation().matrix(),
            self._backend_instance.velocity(),
        )


class Point3D(OptimizableVertex):
    def __init__(self, index: int, value: Vector3 = zero_vector3):
        """
        Args:
            index: index of the vertex.

            value: x,y,z coordinates.
        """
        super().__init__(index, value)

    @property
    def value(self) -> Vector3:
        """Position of the point: x, y, z."""
        return self._value

    @property
    def backend_instance(self) -> Vector3:
        """Identical to the value property, as GTSAM does not have a separate class for
        point in 3D."""
        return self._value

    @property
    def backend_index(self) -> int:
        """GTSAM instance index."""
        return P(self._index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the point with the new value.

        Args:
            value: GTSAM values.
        """
        self._value = value.atPoint3(self.backend_index)


class ImuBias(OptimizableVertex):
    """Imu bias in Graph."""

    def __init__(self, index: int, value: tuple[Vector3, Vector3] = (zero_vector3, zero_vector3)):
        """
        Args:
            index: index of the vertex.

            value: accelerometer bias, gyroscope bias.
        """
        super().__init__(index, value)
        self._backend_instance = gtsam.imuBias.ConstantBias(value[0], value[1])

    @property
    def value(self) -> tuple[Vector3, Vector3]:
        """Accelerometer and gyroscope biases: (Ax, Ay, Az), (Gx, Gy, Gz)."""
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
        return B(self._index)

    def update(self, value: gtsam.Values) -> None:
        """Updates the Imu bias with the new value.

        Args:
            value: GTSAM values.
        """
        self._backend_instance = value.atConstantBias(self.backend_index)
        self._value = self._backend_instance.accelerometer(), self._backend_instance.gyroscope()


class Feature3D(NonOptimizableVertex):
    """Non-optimizable point in 3D."""

    def __init__(self, index: int, value: Vector3 = zero_vector3):
        """
        Args:
            index: index of the vertex.

            value: x,y,z coordinates.
        """
        super().__init__(index, value)

    @property
    def value(self) -> Vector3:
        """Position of the feature: x, y, z."""
        return self._value

    def update(self, value: Vector3) -> None:
        """Updates the feature with the new value.

        Args:
            value: New value of the feature.
        """
        self._value = value
