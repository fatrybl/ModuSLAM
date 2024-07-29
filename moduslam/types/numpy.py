"""Numpy type aliases."""

from typing import Annotated, Literal

import numpy as np
import numpy.typing as npt

Vector2 = Annotated[npt.NDArray[np.floating | np.integer], Literal[2]]
Vector3 = Annotated[npt.NDArray[np.floating | np.integer], Literal[3]]
VectorN = Annotated[npt.NDArray[np.floating | np.integer], Literal["N"]]

Matrix3x3 = Annotated[npt.NDArray[np.floating | np.integer], Literal[3, 3]]
Matrix4x4 = Annotated[npt.NDArray[np.floating | np.integer], Literal[4, 4]]
Matrix6x6 = Annotated[npt.NDArray[np.floating | np.integer], Literal[6, 6]]
MatrixNx2 = Annotated[npt.NDArray[np.floating | np.integer], Literal["N", 2]]
MatrixNx3 = Annotated[npt.NDArray[np.floating | np.integer], Literal["N", 3]]
Matrix3xN = Annotated[npt.NDArray[np.floating | np.integer], Literal[3, "N"]]
Matrix4xN = Annotated[npt.NDArray[np.floating | np.integer], Literal[4, "N"]]
MatrixNx4 = Annotated[npt.NDArray[np.floating | np.integer], Literal["N", 4]]
MatrixNxN = Annotated[npt.NDArray[np.floating | np.integer], Literal["N", "N"]]
MatrixMxN = Annotated[npt.NDArray[np.floating | np.integer], Literal["M", "N"]]
