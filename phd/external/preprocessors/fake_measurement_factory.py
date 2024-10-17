from collections.abc import Iterable
from typing import cast

from phd.external.objects.auxiliary_objects import Connection
from phd.external.objects.measurements import (
    ContinuousMeasurement,
    FakeMeasurement,
    Measurement,
)
from phd.external.utils import get_subsequence


def create_fake(measurement: ContinuousMeasurement) -> FakeMeasurement:
    """Creates a fake measurement.

    Args:
        measurement: measurement to be used for fake measurement.

    Returns:
        fake measurement.
    """
    t = measurement.time_range.start
    return FakeMeasurement(t)


def find_fake_measurement(measurements: Iterable[Measurement]) -> FakeMeasurement | None:
    """Finds the 1-st fake measurement in the sequence of measurements.

    Args:
        measurements: sequence of measurements.

    Returns:
        the 1-st fake measurement if found or None.
    """
    for m in measurements:
        if m.value == FakeMeasurement.fake_value:
            m = cast(FakeMeasurement, m)
            return m
    return None


def process_single_fake(
    connection: Connection,
    measurement: ContinuousMeasurement,
    fake_measurement: FakeMeasurement,
):
    """Processes a connection with the 1-st cluster having a fake measurement.

    Args:
        connection: connection to be processed.

        measurement: continuous measurement to be used for connection.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used measurements and empty cluster.
    """
    cluster1 = connection.cluster1
    cluster2 = connection.cluster2
    start = fake_measurement.timestamp
    stop = cluster2.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster2.add(new_measurement)
    return elements, cluster1


def process_fake_and_non_fake(
    connection: Connection,
    measurement: ContinuousMeasurement,
    fake_measurement: FakeMeasurement,
):
    """Processes a connection when the 1-st cluster has both fake and real measurements.

    Args:
        connection: connection to be processed.

        measurement: continuous measurement to be used for connection.

        fake_measurement: fake measurement to be used for connection.

    Returns:
        used elements.
    """
    used_elements = []
    cluster1 = connection.cluster1
    cluster2 = connection.cluster2
    start = fake_measurement.timestamp
    stop = cluster1.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    if len(elements) > 0:
        new_measurement = ContinuousMeasurement(elements)
        cluster1.add(new_measurement)
        used_elements += elements

    cluster1.remove(fake_measurement)

    start = cluster1.timestamp
    stop = cluster2.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster2.add(new_measurement)
    used_elements += elements
    return used_elements


def process_non_fake(connection: Connection, measurement: ContinuousMeasurement):
    """Processes a connection when the 1-st cluster has no fake measurement.

    Args:
        connection: connection to be processed.

        measurement: continuous measurement to be used for connection.

    Returns:
        used elements.
    """
    cluster1 = connection.cluster1
    cluster2 = connection.cluster2
    start = cluster1.timestamp
    stop = cluster2.timestamp
    elements, _, stop = get_subsequence(measurement.elements, start, stop)
    new_measurement = ContinuousMeasurement(elements)
    cluster2.add(new_measurement)
    return elements
