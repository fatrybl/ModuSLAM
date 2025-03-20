"""Module for collecting measurements from the data sources for Kaist Urban Dataset."""

import logging
from collections.abc import Callable

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.readers.data_sources import (
    CsvData,
    PointCloudData,
    Source,
    StereoImageData,
)
from src.moduslam.data_manager.batch_factory.readers.kaist.utils import (
    get_csv_message_by_location,
    get_pointcloud_message_by_location,
    get_stereo_message_by_location,
    read_binary,
)
from src.moduslam.data_manager.batch_factory.readers.locations import (
    BinaryDataLocation,
    CsvDataLocation,
    Location,
    StereoImagesLocation,
)
from src.moduslam.data_manager.batch_factory.readers.utils import (
    get_csv_message,
    get_images,
)
from src.utils.auxiliary_dataclasses import Message

logger = logging.getLogger(data_manager)


def get_next_measurement(
    source: Source,
) -> tuple[Message, CsvDataLocation | BinaryDataLocation | StereoImagesLocation]:
    """Gets the next measurement from the data source.

    Args:
        source: Data source.

    Returns:
        message and location.

    Raises:
        StopIteration: if the data source has exhausted.
    """
    source_getter_table: dict[type, tuple[Callable, str]] = {
        CsvData: (get_csv_measurement, "CSV data has finished."),
        PointCloudData: (get_pointcloud_measurement, "Pointcloud data has finished."),
        StereoImageData: (get_stereo_measurement, "Stereo images have finished."),
    }

    measurement_getter, msg = source_getter_table[type(source)]

    try:
        message, location = measurement_getter(source)
    except StopIteration:
        logger.debug(msg)
        raise StopIteration(msg)

    return message, location


def get_measurement(location: Location) -> Message:
    """Gets the measurement by the location.

    Args:
        location: Data location.

    Returns:
        a message.
    """
    location_method_table: dict[type, Callable] = {
        CsvDataLocation: get_csv_message_by_location,
        BinaryDataLocation: get_pointcloud_message_by_location,
        StereoImagesLocation: get_stereo_message_by_location,
    }
    message_getter = location_method_table[type(location)]
    message = message_getter(location)
    return message


def get_csv_measurement(source: CsvData) -> tuple[Message, CsvDataLocation]:
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

    message = get_csv_message(line, separator=",")
    location = CsvDataLocation(source.file, source.position)
    return message, location


def get_pointcloud_measurement(source: PointCloudData) -> tuple[Message, BinaryDataLocation]:
    """Gets the next point cloud measurement.

    Args:
        source: point cloud data source.

    Returns:
        message and location.

    Raises:
        StopIteration: if the point cloud data has finished.
    """
    try:
        file = next(source)
    except StopIteration:
        raise

    timestamp = file.stem
    data = read_binary(file)
    message = Message(timestamp, data)
    location = BinaryDataLocation(file)
    return message, location


def get_stereo_measurement(source: StereoImageData) -> tuple[Message, StereoImagesLocation]:
    """Gets the next stereo image measurement.

    Args:
        source: Stereo image data source.

    Returns:
        message and location.

    Raises:
        StopIteration: if the stereo image data has finished.
    """

    try:
        left_image_file, right_image_file = next(source)
    except StopIteration:
        raise

    timestamp_left, _ = left_image_file.stem, right_image_file.stem
    images = get_images(left_image_file, right_image_file)
    message = Message(timestamp_left, images)
    location = StereoImagesLocation(source.files)
    return message, location
