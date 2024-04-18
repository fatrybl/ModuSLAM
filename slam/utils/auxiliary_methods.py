import logging
from importlib import import_module

import gtsam
import numpy as np
from PIL.Image import Image

from slam.data_manager.factory.element import Element
from slam.utils.exceptions import DimensionalityError

logger = logging.getLogger(__name__)


def vector_3(x, y, z):
    """Creates 3D float64 numpy array."""
    return np.array([x, y, z], dtype=np.float64)


def vector_n(*args):
    """Create N-dimensional float64 numpy array."""
    return np.array(args, dtype=np.float64)


def tuple_to_gtsam_pose3(values: tuple[float, float, float, float, float, float]) -> gtsam.Pose3:
    """Converts a tuple of (x, y, z, roll, pitch, yaw) to a gtsam.Pose3 object.

    Args:
        values (tuple[float, float, float, float, float, float]:
                tuple with values [x, y, z, roll, pitch, yaw].

    Returns:
        gtsam.Pose3.
    """
    rotation = gtsam.Rot3.Ypr(values[5], values[4], values[3])
    position = values[:3]
    pose = gtsam.Pose3(rotation, position)
    return pose


def as_int(value: str) -> int:
    """
    Converts value to int.
    Args:
        value (str): input value.

    Returns:
        (int): converted value.
    """
    try:
        int_value: int = int(value)
        return int_value
    except ValueError:
        msg = f"Could not convert value {value} of type {type(value)} to string"
        logger.error(msg)
        raise


def check_dimensionality(array: np.ndarray, shape: tuple[int, ...]) -> None:
    """Checks if the array has the required shape.

    Args:
        array (np.ndarray): array to check.
        shape (tuple[int, ...]): required shape.

    Raises:
        DimensionalityError: if the array has a wrong shape.

    TODO: add tests.
    """
    if array.shape != shape:
        msg = f"Array must have shape {shape}, got {array.shape}"
        logger.critical(msg)
        raise DimensionalityError(msg)


def equal_images(imgs_1: tuple[Image, ...], imgs_2: tuple[Image, ...]) -> bool:
    """Compares two elements with Image data.

    PIL images can not be compared directly because of different subclasses.
    Manually created image from numpy.array is of type Image.Image,
    but the one obtained from file is of type PIL.PngImagePlugin.PngImageFile.

    Args:
        imgs_1 (tuple[Image, ...]): 1-st tuple with images.
        imgs_2 (tuple[Image, ...]): 2-nd tuple with images.

    Returns:
        bool: comparison result
    """

    assert len(imgs_1) == len(imgs_2), "Tuples have different number of images."

    for img1, img2 in zip(imgs_1, imgs_2):
        array_img1 = np.asarray(img1)
        array_img2 = np.asarray(img2)
        if np.array_equal(array_img1, array_img2) is False:
            return False
    return True


def equal_elements(el1: Element | None, el2: Element | None) -> bool:
    """
    Compares two elements by the following fields:
    - timestamp
    - location
    - measurement.sensor
    - measurement.values

    If the values are of type Image, they are compared separately with equal_images() method.

    Args:
        el1 (Element): 1-st element.
        el2 (Element): 2-nd element.

    Returns:
        bool: comparison result.
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


def import_object(object_name: str, module_name: str, package_name: str) -> type:
    """
    Imports object with the given name.
    Args:
        object_name (str): class name.
        module_name (str): name of the module to import from.
        package_name (str): name of the package to import a module from.

    Returns:
        (type): imported object.
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
