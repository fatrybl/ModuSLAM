"""Numpy type aliases."""

from typing import Annotated, Literal

import numpy as np
from numpy.typing import NDArray

Vector2 = Annotated[NDArray[np.floating | np.integer], Literal[2]]
Vector3 = Annotated[NDArray[np.floating | np.integer], Literal[3]]
VectorN = Annotated[NDArray[np.floating | np.integer], Literal["N"]]

Matrix3x3 = Annotated[NDArray[np.floating | np.integer], Literal[3, 3]]
Matrix4x4 = Annotated[NDArray[np.floating | np.integer], Literal[4, 4]]
Matrix6x6 = Annotated[NDArray[np.floating | np.integer], Literal[6, 6]]
MatrixNx2 = Annotated[NDArray[np.floating | np.integer], Literal["N", 2]]
MatrixNx3 = Annotated[NDArray[np.floating | np.integer], Literal["N", 3]]
Matrix3xN = Annotated[NDArray[np.floating | np.integer], Literal[3, "N"]]
Matrix4xN = Annotated[NDArray[np.floating | np.integer], Literal[4, "N"]]
MatrixNx4 = Annotated[NDArray[np.floating | np.integer], Literal["N", 4]]
MatrixNxN = Annotated[NDArray[np.floating | np.integer], Literal["N", "N"]]
MatrixMxN = Annotated[NDArray[np.floating | np.integer], Literal["M", "N"]]
