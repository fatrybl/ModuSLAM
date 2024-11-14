from collections.abc import Iterable

from phd.exceptions import NotEnoughMeasurementsError
from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import Measurement
from phd.moduslam.data_manager.batch_factory.batch import DataBatch, Element
from phd.moduslam.frontend_manager.handlers.handler_protocol import Handler
from phd.moduslam.frontend_manager.measurement_storage_analyzers.base import (
    StorageAnalyzer,
)


def distribute_element(handlers: Iterable[Handler], element: Element) -> Measurement | None:
    """Processes an element with the appropriate handler.

    Args:
        handlers:

        element: element to be distributed and processed.

    Returns:
        new measurement or None.
    """
    sensor = element.measurement.sensor

    for handler in handlers:
        if handler.sensor_type == type(sensor) and handler.sensor_name == sensor.name:

            new_measurement = handler.process(element)

            if new_measurement:
                return new_measurement

    return None


def fill_storage(
    storage: MeasurementStorage,
    data: DataBatch,
    handlers: Iterable[Handler],
    analyzer: StorageAnalyzer,
) -> None:
    """Fills the storage with the measurements created by handlers using the given data.
    The storage is filled based on the analyzer`s decision.

    Args:
        storage: a storage to add measurements to.

        data: a data batch with elements.

        handlers: handlers to create measurements.

        analyzer: an analyzer to decide if the storage is filled.

    Raises:
        NotEnoughMeasurementsError: not enough data to fill the storage.
    """
    enough_measurements = False
    while not enough_measurements and not data.empty:
        element = data.first
        data.remove_first()
        new_measurement = distribute_element(handlers, element)

        storage.add(new_measurement) if new_measurement else None

        enough_measurements = analyzer.check_storage(storage)
        if enough_measurements:
            return

    raise NotEnoughMeasurementsError
