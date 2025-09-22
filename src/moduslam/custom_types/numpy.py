"""Numpy type aliases."""

from typing import Annotated, Literal, TypeVar

import numpy as np
from numpy.typing import NDArray

# Define type variables for dynamic dimensions
N = TypeVar("N", bound=int)  # Represents a generic integer dimension
M = TypeVar("M", bound=int)  # Represents another generic integer dimension

# Vector type aliases
Vector2 = Annotated[NDArray[np.floating | np.integer], Literal[2]]
Vector3 = Annotated[NDArray[np.floating | np.integer], Literal[3]]
VectorN = Annotated[NDArray[np.floating | np.integer], N]  # Generic 1D array

# Matrix type aliases
Matrix3x3 = Annotated[NDArray[np.floating | np.integer], Literal[3, 3]]
Matrix4x4 = Annotated[NDArray[np.floating | np.integer], Literal[4, 4]]
Matrix6x6 = Annotated[NDArray[np.floating | np.integer], Literal[6, 6]]
MatrixNx2 = Annotated[NDArray[np.floating | np.integer], (N, 2)]  # N rows, 2 columns
MatrixNx3 = Annotated[NDArray[np.floating | np.integer], (N, 3)]  # N rows, 3 columns
Matrix3xN = Annotated[NDArray[np.floating | np.integer], (3, N)]  # 3 rows, N columns
Matrix4xN = Annotated[NDArray[np.floating | np.integer], (4, N)]  # 4 rows, N columns
MatrixNx4 = Annotated[NDArray[np.floating | np.integer], (N, 4)]  # N rows, 4 columns
MatrixNxN = Annotated[NDArray[np.floating | np.integer], (N, N)]  # N x N matrix
MatrixMxN = Annotated[NDArray[np.floating | np.integer], (M, N)]  # M x N matrix
