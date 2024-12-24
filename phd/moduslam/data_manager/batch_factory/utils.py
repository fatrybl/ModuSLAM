from PIL.Image import Image

from phd.moduslam.data_manager.batch_factory.batch import DataBatch
from phd.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from phd.utils.auxiliary_methods import equal_images


def create_empty_element(element: Element) -> Element:
    """Creates an empty element with the same timestamp, location and sensor as the
    input element.

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
