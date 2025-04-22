import numpy as np

from src.moduslam.data_manager.batch_factory.batch import DataBatch
from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement


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


def equal_elements(element1: Element | None, element2: Element | None) -> bool:
    """Compares two elements.

    Args:
        element1: 1-st element.

        element2: 2-nd element.

    Returns:
        comparison result.
    """
    if element1 is None and element2 is None:
        return True

    if element1 is None or element2 is None:
        return False

    t1, t2 = element1.timestamp, element2.timestamp
    loc1, loc2 = element1.location, element2.location
    sens1, sens2 = element1.measurement.sensor, element2.measurement.sensor
    val1 = np.asarray(element1.measurement.values)
    val2 = np.asarray(element2.measurement.values)

    return t1 == t2 and loc1 == loc2 and sens1 == sens2 and np.array_equal(val1, val2)


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
