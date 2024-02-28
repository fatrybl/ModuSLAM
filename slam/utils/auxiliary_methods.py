import logging
from importlib import import_module

import numpy as np
from PIL.Image import Image

from slam.data_manager.factory.element import Element

logger = logging.getLogger(__name__)


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


def equal_images(el1: Element, el2: Element) -> bool:
    """Compares two elements with Image data.

    PIL images can not be compared directly because of different subclasses.
    Manually created image from numpy.array is of type Image.Image,
    but the one obtained from file is of type PIL.PngImagePlugin.PngImageFile.

    Args:
        el1 (Element): 1-st element to be compared.
        el2 (Element): 2-nd element to be compared.

    Returns:
        bool: comparison result
    """

    assert len(el1.measurement.values) == len(
        el2.measurement.values
    ), "Elements have different number of images."

    for img1, img2 in zip(el1.measurement.values, el2.measurement.values):
        array_img1 = np.asarray(img1)
        array_img2 = np.asarray(img2)
        if np.array_equal(array_img1, array_img2) is False:
            return False
    return True


def equal_elements(el1: Element | None, el2: Element | None):
    if el1 is None and el2 is None:
        assert True

    elif el1 is not None and el2 is not None:
        if isinstance(el1.measurement.values[0], Image):
            assert equal_images(el1, el2) is True
        else:
            assert el1.measurement.values == el2.measurement.values

        assert el1.timestamp == el2.timestamp
        assert el1.location == el2.location
        assert el1.measurement.sensor == el2.measurement.sensor

    else:
        assert False, "Either element 1 or element 2 is None."


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
