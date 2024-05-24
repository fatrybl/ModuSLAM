from typing import Annotated, Literal

import numpy as np
import numpy.typing as npt

Vector2 = Annotated[npt.NDArray[np.float64], Literal[2]]
Vector3 = Annotated[npt.NDArray[np.float64], Literal[3]]
VectorN = Annotated[npt.NDArray[np.float64], Literal["N"]]

Matrix3x3 = Annotated[npt.NDArray[np.float64], Literal[3, 3]]
Matrix4x4 = Annotated[npt.NDArray[np.float64], Literal[4, 4]]
MatrixNxN = Annotated[npt.NDArray[np.float64], Literal["N", "N"]]
