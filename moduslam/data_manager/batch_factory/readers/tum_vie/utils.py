import logging
from pathlib import Path

from PIL.Image import Image

from moduslam.data_manager.batch_factory.readers.locations import (
    CsvDataLocation,
    StereoImagesLocation,
)
from moduslam.data_manager.batch_factory.readers.utils import get_images, read_csv_file
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit
from moduslam.utils.auxiliary_methods import microsec2nanosec

logger = logging.getLogger(data_manager)


def get_csv_data_by_location(location: CsvDataLocation) -> tuple[str, ...]:
    """Gets csv data by location.

    Args:
        location: location of the csv data.

    Returns:
        message: a message with csv data.
    """
    file = location.file
    num_lines = location.position
    with open(file, "r") as f:
        next(f)  # skip header
        for _ in range(num_lines):
            line = next(f)
        line = line.strip()
        data = line.split()[1:]
        return tuple(data)


def get_stereo_data_by_location(location: StereoImagesLocation) -> tuple[Image, Image]:
    """Gets stereo images by location.

    Args:
        location: location of the stereo images.

    Returns:
        message: a message containing the stereo images.
    """
    left_image_file, right_image_file = location.files[0], location.files[1]
    images = get_images(left_image_file, right_image_file)
    return images


def get_timestamp(line: list[str]) -> int:
    """Gets timestamp from a row.

    Args:
        line: contains raw data.
    """
    timestamp = microsec2nanosec(line[0])
    return timestamp


def create_sequence(
    files: dict[str, Path],
    regime: TimeLimit | Stream,
    used_sensors: set[str],
) -> tuple[list[tuple[int, str, int]], dict[str, int]]:
    """Create a list of tuples containing the timestamp, sensor name and index.

    Args:
        files: dict with sensor names and file paths.

        regime: a TimeLimit or Stream object.

        used_sensors: a set of sensor names to be used.

    Returns:
        elements: a list of tuples containing the timestamp, sensor name and index.

        sensor_indices: a dictionary of sensor name and index pairs.
    """

    elements: list[tuple[int, str, int]] = []
    sensors_indices: dict[str, int] = {}
    latest_sensors_indices: dict[str, int] = {}
    default_index: int = 0

    for sensor_name, file in files.items():
        if sensor_name not in used_sensors:
            continue

        lines = read_csv_file(file, delimiter=" ")
        next(lines)  # Skip header

        for line in lines:
            timestamp = get_timestamp(line)
            index = sensors_indices.get(sensor_name, default_index) + 1
            sensors_indices[sensor_name] = index

            if isinstance(regime, TimeLimit):
                if timestamp < regime.start:
                    latest_sensors_indices[sensor_name] = index

                if regime.start <= timestamp <= regime.stop:
                    elements.append((timestamp, sensor_name, index))
                    if sensor_name not in latest_sensors_indices:
                        latest_sensors_indices[sensor_name] = default_index

            else:
                latest_sensors_indices[sensor_name] = default_index
                elements.append((timestamp, sensor_name, index))

    if len(elements) == 0:
        latest_sensors_indices = {}
    else:
        elements.sort(key=lambda x: x[0])

    return elements, latest_sensors_indices
