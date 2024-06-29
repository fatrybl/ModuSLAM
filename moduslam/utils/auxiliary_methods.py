"""Auxiliary methods for the moduslam package.

Any method used in multiple modules/packages may be defined here.
"""

import logging
import re
from importlib import import_module
from pathlib import Path
from typing import overload

import gtsam
import numpy as np
from PIL.Image import Image
from plum import dispatch

from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.data_manager.batch_factory.element import Element, RawMeasurement
from moduslam.logger.logging_config import utils
from moduslam.utils.exceptions import DimensionalityError
from moduslam.utils.numpy_types import Vector3, VectorN

logger = logging.getLogger(utils)


def create_empty_element(element: Element) -> Element:
    """Creates an empty element with the same timestamp, location and sensor as the input element.
    Args:
        element: input element with data.

    Returns:
        element without data.
    """
    empty_measurement = RawMeasurement(sensor=element.measurement.sensor, values=())
    empty_element = Element(
        timestamp=element.timestamp,
        measurement=empty_measurement,
        location=element.location,
    )
    return empty_element


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


@overload
def microsec2nanosec(microseconds: int | float) -> int:
    return int(microseconds * 1e3)


@overload
def microsec2nanosec(microseconds: str) -> int:
    microsec_float = to_float(microseconds)
    return microsec2nanosec(microsec_float)


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

    return abs(n1 - n2) <= abs(epsilon)


def create_vector_3(x, y, z) -> Vector3:
    """Creates 3D float64 numpy array."""
    return np.array([x, y, z], dtype=np.float64)


def create_vector_n(*args) -> VectorN:
    """Creates N-dimensional float64 numpy array."""
    return np.array(args, dtype=np.float64)


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


def to_float(value: str) -> float:
    """Converts value to float.

    Args:
        value: input value.

    Returns:
        float value.

    Raises:
        ValueError: if the value can not be converted to float.
    """
    try:
        float_value = float(value)
        return float_value

    except ValueError:
        msg = f"Could not convert value {value} of type {type(value)} to float."
        logger.critical(msg)
        raise


def to_int(value: str) -> int:
    """Converts value to int.

    Args:
        value: input value.

    Returns:
        int value.

    Raises:
        ValueError: if the value can not be converted to int.
    """
    try:
        int_value = int(value)
        return int_value

    except ValueError:
        msg = f"Could not convert value {value} of type {type(value)} to string."
        logger.critical(msg)
        raise


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


def equal_images(imgs_1: tuple[Image, ...], imgs_2: tuple[Image, ...]) -> bool:
    """Compares two items with Image data.

    PIL images can not be compared directly because of different subclasses.
    Manually created image from numpy.array is of type Image.Image,
    but the one obtained from file is of type PIL.PngImagePlugin.PngImageFile.

    Args:
        imgs_1: 1-st tuple with images.

        imgs_2: 2-nd tuple with images.

    Returns:
        equality result.

    Raises:
        DimensionalityError: if the tuples have different number of images.
    """

    if len(imgs_1) != len(imgs_2):
        msg = "Tuples have different number of images."
        logger.critical(msg)
        raise DimensionalityError(msg)

    for img1, img2 in zip(imgs_1, imgs_2):
        array_img1 = np.asarray(img1)
        array_img2 = np.asarray(img2)
        if np.array_equal(array_img1, array_img2) is False:
            return False

    return True


def equal_elements(el1: Element | None, el2: Element | None) -> bool:
    """Compares two elements.

    If the values are of type Image, they are compared separately with equal_images() method.

    Args:
        el1: 1-st element.

        el2: 2-nd element.

    Returns:
        comparison result.
    """
    if el1 is None and el2 is None:
        return True

    elif el1 is not None and el2 is not None:
        if isinstance(el1.measurement.values[0], Image):
            if equal_images(el1.measurement.values, el2.measurement.values) is False:
                return False
        else:
            if el1.measurement.values != el2.measurement.values:
                return False

        if el1.timestamp != el2.timestamp:
            return False
        if el1.location != el2.location:
            return False
        if el1.measurement.sensor != el2.measurement.sensor:
            return False

    else:
        return False

    return True


def equal_batches(batch1: DataBatch, batch2: DataBatch) -> bool:
    """Compares two data batches.

    Args:
        batch1: 1-st data batch.

        batch2: 2-nd data batch.

    Returns:
        comparison result.
    """
    if batch1.empty and batch2.empty:
        return True

    if len(batch1.data) != len(batch2.data):
        return False

    for el1, el2 in zip(batch1.data, batch2.data):
        if not equal_elements(el1, el2):
            return False

    return True


def import_object(object_name: str, module_name: str, package_name: str) -> type:
    """Imports object.

    Args:
        object_name: class name.

        module_name: name of the module to import from.

        package_name: name of the package to import a module from.

    Returns:
        imported object.

    Raises:
        ModuleNotFoundError: if the module is not found.

        AttributeError: if the object is not found in the module.
    """
    try:
        module = import_module(name=module_name, package=package_name)
    except ModuleNotFoundError:
        msg = f"Module {module_name!r} not found in package {package_name!r}."
        logger.error(msg)
        raise

    try:
        obj: type = getattr(module, object_name)
        return obj
    except AttributeError:
        msg = f"Object {object_name!r} not found in module {module_name!r}."
        logger.error(msg)
        raise


def sort_files_numerically(files: list[Path]) -> list[Path]:
    """Sorts files numerically.

    Args:
        files: list of files to sort.

    Returns:
        sorted list of files.
    """

    def extract_number(file: Path) -> int:
        match = re.search(r"\d+", file.stem)
        return to_int(match.group()) if match else 0

    return sorted(files, key=extract_number)
