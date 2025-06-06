import logging
from collections.abc import Callable

from PIL.Image import Image

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.data_readers.data_sources import Source
from src.moduslam.data_manager.batch_factory.data_readers.locations import (
    CsvDataLocation,
    Location,
    StereoImagesLocation,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.source import (
    TumVieCsvData,
    TumVieStereoImageData,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.utils import (
    get_csv_data_by_location,
    get_stereo_data_by_location,
)
from src.moduslam.data_manager.batch_factory.data_readers.utils import (
    get_csv_message,
    get_images,
)
from src.utils.auxiliary_dataclasses import Message

logger = logging.getLogger(data_manager)


def get_next_measurement(
    source: Source,
) -> tuple[Message, CsvDataLocation | StereoImagesLocation]:
    """Gets the next measurement from the data source.

    Args:
        source: Data source.

    Returns:
        message and location.

    Raises:
        StopIteration: if the data source has exhausted.
    """
    source_getter_table: dict[type, tuple[Callable, str]] = {
        TumVieCsvData: (get_csv_measurement, "CSV data has finished."),
        TumVieStereoImageData: (get_stereo_measurement, "Stereo images have finished."),
    }

    message_getter, msg = source_getter_table[type(source)]

    try:
        message, location = message_getter(source)
    except StopIteration:
        logger.debug(msg)
        raise StopIteration(msg)

    return message, location


def get_measurement(location: Location) -> tuple[str, ...] | tuple[Image, Image]:
    """Gets the measurement by the location.

    Args:
        location: Data location.

    Returns:
        message.
    """
    location_method_table: dict[type, Callable] = {
        CsvDataLocation: get_csv_data_by_location,
        StereoImagesLocation: get_stereo_data_by_location,
    }
    data_getter = location_method_table[type(location)]
    data = data_getter(location)
    return data


def get_csv_measurement(source: TumVieCsvData) -> tuple[Message, CsvDataLocation]:
    """Gets the next CSV measurement.

    Args:
        source: CSV data source.

    Returns:
        message and location.

    Raises:
        StopIteration: if the CSV data has finished.
    """
    try:
        line = next(source)
    except StopIteration:
        raise

    message = get_csv_message(line)
    location = CsvDataLocation(source.file, source.position)
    return message, location


def get_stereo_measurement(source: TumVieStereoImageData) -> tuple[Message, StereoImagesLocation]:
    """Gets the next stereo image measurement.

    Args:
        source: Stereo image data source.

    Returns:
        message and location.

    Raises:
        StopIteration: if the stereo image data has finished.
    """

    try:
        left_img_file, right_img_file, timestamp = next(source)
    except StopIteration:
        raise

    images = get_images(left_img_file, right_img_file)
    message = Message(timestamp=timestamp, data=images)
    location = StereoImagesLocation(source.files)
    return message, location
