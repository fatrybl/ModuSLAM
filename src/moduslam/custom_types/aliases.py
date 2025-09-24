"""Type aliases."""

from typing import TypeAlias

Pixel2D: TypeAlias = tuple[int, int]
Point2D: TypeAlias = tuple[float, float]
Point3D: TypeAlias = tuple[float, float, float]

Vector3: TypeAlias = tuple[float, float, float]
Vector6: TypeAlias = tuple[float, float, float, float, float, float]
VectorN: TypeAlias = tuple[float, ...]

Matrix3x3: TypeAlias = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]

Matrix4x4: TypeAlias = tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]

Matrix6x6: TypeAlias = tuple[
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
    tuple[float, float, float, float, float, float],
]
