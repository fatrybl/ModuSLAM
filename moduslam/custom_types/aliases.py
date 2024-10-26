"""Type aliases."""

from typing import TypeAlias

Point3D: TypeAlias = tuple[float, float, float]

Vector3: TypeAlias = tuple[float, float, float]

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
