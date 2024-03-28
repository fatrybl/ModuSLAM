from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TypeAlias, TypeVar

import gtsam
import numpy as np
from gtsam.symbol_shorthand import B, L, N, P, V, X

from slam.utils.numpy_types import Matrix3x3, Matrix4x4, Vector3

GtsamVertex: TypeAlias = gtsam.Rot3 | gtsam.Pose3 | gtsam.NavState


def vector_3(x, y, z):
    """Create 3d double numpy array."""
    return np.array([x, y, z], dtype=np.float64)


def vector_n(*args):
    """Create N-dimensional double numpy array."""
    return np.array(args, dtype=np.float64)


class Vertex(ABC):
    """Base absract vertex of the Graph.

    TODO: think about numpy types for the attributes.
    """

    def __init__(self):
        self.index: int = 0
        self.timestamp: int = 0
        self.edges = set()
        self.optimizable: bool = False
        self.value: Any = None

    @abstractmethod
    def update(self, values: Any) -> None:
        """Updates the vertex with the new values.

        Args:
            values (Any): new values.
        """


class Pose(Vertex):
    """Pose vertex in Graph.

    TODO: check types of the attributes.
    """

    def __init__(self):
        super().__init__()
        self.optimizable = True
        self.value: GtsamVertex = gtsam.Pose3()
        self.position: Vector3 = self.value.translation
        self.rotation: Matrix3x3 = self.value.rotation
        self.SE3: Matrix4x4 = self.value.matrix

    @property
    def gtsam_index(self) -> int:
        return X(self.index)

    def update(self, values: gtsam.Values) -> None:
        self.value = values.atPose3(self.gtsam_index)
        self.position = self.value.translation()
        self.rotation = self.value.rotation()
        self.SE3 = self.value.matrix()


class CameraPose(Pose):
    """The pose where an image has been taken."""


class LidarPose(Pose):
    """The pose where a point-cloud has been registered."""


class Velocity(Vertex):
    """Linear velocity vertex in Graph."""

    def __init__(self):
        super().__init__()
        self.optimizable = True
        self.value = vector_3(0.0, 0.0, 0.0)

    @property
    def gtsam_index(self) -> int:
        return V(self.index)

    def update(self, values: gtsam.Values) -> None:
        self.value = values.atVector(self.gtsam_index)


class NavState(Vertex):
    """
    Navigation state vertex in the Graph:
        pose and velocity.
    """

    def __init__(self):
        super().__init__()
        self.value: gtsam.NavState = gtsam.NavState()
        self.velocity = self.value.velocity()
        self.pose = self.value.pose()

    @property
    def gtsam_index(self) -> int:
        return N(self.index)

    def update(self, values: gtsam.Values) -> None:
        self.value = values.atNavState(self.gtsam_index)
        self.velocity = self.value.velocity()
        self.pose = self.value.pose()


class Point(Vertex):
    def __init__(self):
        super().__init__()
        self.optimizable = True
        self.value: gtsam.Point3 = gtsam.Point3()

    @property
    def gtsam_index(self) -> int:
        return P(self.index)

    def update(self, values: gtsam.Values) -> None:
        self.value = values.atPoint3(self.gtsam_index)


class PoseLandmark(Pose):
    """Base landmark in the Graph."""

    @property
    def gtsam_index(self) -> int:
        return L(self.index)


class Feature(Vertex):
    """Non-optimizable point in 3D."""

    def __init__(self):
        super().__init__()
        self.position: Vector3 = vector_3(0.0, 0.0, 0.0)

    def update(self, values) -> None: ...


class CameraFeature(Feature):
    """Feature in the Camera Frame."""


class ImuBias(Vertex):
    """Imu bias in the Graph."""

    def __init__(self):
        super().__init__()
        self.optimizable = True
        self.value: gtsam.imuBias = gtsam.imuBias.ConstantBias()
        self.accelerometer_bias = self.value.accelerometer()
        self.gyroscope_bias = self.value.gyroscope()

    @property
    def gtsam_index(self) -> int:
        return B(self.index)

    def update(self, values: gtsam.Values) -> None:
        self.value = values.atConstantBias(self.gtsam_index)
        self.accelerometer_bias = self.value.accelerometer()
        self.gyroscope_bias = self.value.gyroscope()


GraphVertex = TypeVar("GraphVertex", bound=Vertex)
