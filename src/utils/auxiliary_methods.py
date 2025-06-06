"""Auxiliary methods for the ModuSLAM package.

Any method used in multiple modules/packages may be defined here.
"""

import functools
import logging
import re
import time
from collections.abc import Callable, Iterable
from functools import wraps
from pathlib import Path
from typing import Any, overload

import gtsam
import numpy as np
from plum import dispatch

from src.custom_types.aliases import Matrix3x3, Matrix4x4, Vector3
from src.custom_types.numpy import Matrix4x4 as NumpyMatrix4x4
from src.custom_types.numpy import (
    MatrixMxN,
)
from src.custom_types.numpy import Vector3 as NumpyVector3
from src.custom_types.numpy import (
    VectorN,
)
from src.logger.logging_config import utils
from src.utils.exceptions import DimensionalityError

logger = logging.getLogger(utils)


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print("Finished {} in {} secs".format(repr(func.__name__), run_time))
        return value

    return wrapper


def exception_handler(custom_exception: type[Exception], message: str) -> Callable:
    """Decorator to handle exceptions and raise a custom exception."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise custom_exception(message) from e

        return wrapper

    return decorator


def matrix4x4_list_to_tuple(matrix: list[list[float]]) -> Matrix4x4:
    """Converts SE(3) transformation matrix represented as a list of lists of floats
    into the tuple of tuples of floats of the fixed shape.

    Args:
        matrix: SE(3) matrix represented as a list of lists of floats.

    Returns:
        Matrix4x4 representing the SE(3) transformation.

    Raises:
        DimensionalityError: if the input matrix has incompatible dimensions.
    """
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise DimensionalityError("Input matrix must be 4x4.")

    return (
        (matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3]),
        (matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3]),
        (matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3]),
        (matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3]),
    )


def matrix3x3_list_to_tuple(matrix: list[list[float]]) -> Matrix3x3:
    """Converts SE(3) transformation matrix represented as a list of lists of floats
    into the tuple of tuples of floats of the fixed shape.

    Args:
        matrix: SE(3) matrix represented as a list of lists of floats.

    Returns:
        Matrix4x4 representing the SE(3) transformation.

    Raises:
        DimensionalityError: if the input matrix has incompatible dimensions.
    """
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise DimensionalityError("Input matrix must be 3x3.")

    return (
        (matrix[0][0], matrix[0][1], matrix[0][2]),
        (matrix[1][0], matrix[1][1], matrix[1][2]),
        (matrix[2][0], matrix[2][1], matrix[2][2]),
    )


def numpy_array4x4_to_tuple4x4(matrix: NumpyMatrix4x4) -> Matrix4x4:
    """Converts numpy matrix of size 4x4 to tuple of tuples of size 4x4.

    Args:
        matrix: numpy matrix of size 4x4.

    Returns:
        tuple of tuples of size 4x4.

    Raises:
        ValueError: if the input array has wrong shape.
    """
    if matrix.shape != (4, 4):
        raise ValueError("Input array must have shape (4, 4)")
    m = matrix
    return (
        (m[0, 0], m[0, 1], m[0, 2], m[0, 3]),
        (m[1, 0], m[1, 1], m[1, 2], m[1, 3]),
        (m[2, 0], m[2, 1], m[2, 2], m[2, 3]),
        (m[3, 0], m[3, 1], m[3, 2], m[3, 3]),
    )


def diagonal_matrix3x3(values: Vector3) -> Matrix3x3:
    """Creates a 3x3 diagonal matrix from 3D vector.

    Args:
        values: 3D vector.

    Returns:
        diagonal matrix.
    """
    return (
        (values[0], 0.0, 0.0),
        (0.0, values[1], 0.0),
        (0.0, 0.0, values[2]),
    )


def make_iterable(obj: Any) -> Iterable[Any]:
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return obj  # Already iterable, return as is
    return [obj]  # Wrap single item in a list


def sec2nanosec(seconds: int | float) -> int:
    """Converts seconds to nanoseconds.

    Args:
        seconds: time in seconds.

    Returns:
        time in nanoseconds.
    """
    return int(seconds * 1e9)


def nanosec2sec(nanoseconds: int) -> float:
    """Converts nanoseconds to seconds.

    Args:
        nanoseconds: time in nanoseconds.

    Returns:
        time in seconds.
    """
    return nanoseconds * 1e-9


def nanosec2microsec(nanoseconds: int) -> float:
    """Converts nanoseconds to microseconds.

    Args:
        nanoseconds: time in nanoseconds.

    Returns:
        time in microseconds.
    """
    return nanoseconds * 1e-3


@overload
def microsec2nanosec(microseconds: int | float) -> int:
    return int(microseconds * 1e3)


@overload
def microsec2nanosec(microseconds: str) -> int:
    microsec_float = str_to_float(microseconds)
    return int(microsec_float * 1e3)


@dispatch
def microsec2nanosec(microseconds: str | int | float):
    """
    @overload.

    Converts microseconds to nanoseconds.

    Args:
        microseconds: time in microseconds.

    Returns:
        (int): time in nanoseconds.
    """


def equal_integers(n1: int, n2: int, epsilon: int) -> bool:
    """Compares two numbers with a given tolerance.

    Args:
        n1: 1-st number.

        n2: 2-nd number.

        epsilon: tolerance (non-negative).

    Returns:
        comparison result.
    """
    if epsilon < 0:
        msg = f"Epsilon must be non-negative, got {epsilon}."
        logger.critical(msg)
        raise ValueError(msg)

    return abs(n1 - n2) <= epsilon


def create_numpy_vector_3(x: int | float, y: int | float, z: int | float) -> NumpyVector3:
    """Creates 3D float64 numpy array."""
    return np.array([x, y, z], dtype=np.float64)


def tuple_to_gtsam_pose3(values: tuple[float, float, float, float, float, float]) -> gtsam.Pose3:
    """Converts a tuple of (x, y, z, roll, pitch, yaw) to gtsam.Pose3 object.

    Args:
        values: (x, y, z, roll, pitch, yaw).

    Returns:
        gtsam.Pose3.
    """
    rotation = gtsam.Rot3.Ypr(values[5], values[4], values[3])
    position = values[:3]
    pose = gtsam.Pose3(rotation, position)
    return pose


def str_to_float(string: str) -> float:
    """Converts string to float.

    Args:
        string: an input string.

    Returns:
        float value.
    """
    return float(string)


def str_to_int(string: str) -> int:
    """Converts string to int.

    Args:
        string: input value.

    Returns:
        int value.
    """
    return int(string)


def check_dimensionality(array: np.ndarray, shape: tuple[int, ...]) -> None:
    """Checks if the array has the required shape.

    Args:
        array: numpy array to check.
        shape: required shape.

    Raises:
        DimensionalityError: if the array has wrong shape.
    """
    if array.shape != shape:
        msg = f"Array must have shape {shape}, got {array.shape}"
        logger.critical(msg)
        raise DimensionalityError(msg)


def sort_files_numerically(files: list[Path]) -> list[Path]:
    """Sorts files numerically.

    Args:
        files: list of files to sort.

    Returns:
        sorted list of files.
    """

    def extract_number(file: Path) -> int:
        match = re.search(r"\d+", file.stem)
        return str_to_int(match.group()) if match else 0

    return sorted(files, key=extract_number)


def matrix_to_vector_list(matrix: MatrixMxN) -> list[VectorN]:
    """Convert a NumPy array of shape (N, M) to a list of N arrays of shape (1, M).

    Args:
        matrix: The input NumPy array of shape (N, M).

    Returns:
        a list of N arrays of shape (1, M).
    """
    num_rows, _ = matrix.shape
    list_of_arrays = [matrix[i : i + 1, :] for i in range(num_rows)]
    return list_of_arrays
