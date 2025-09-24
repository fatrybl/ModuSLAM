from pathlib import Path

import numpy as np

from moduslam.data_manager.batch_factory.data_readers.locations import (
    BinaryDataLocation,
    CsvDataLocation,
    StereoImagesLocation,
)
from moduslam.data_manager.batch_factory.data_readers.utils import (
    get_csv_message,
    get_images,
    read_csv_file,
)
from moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.utils.auxiliary_dataclasses import Message
from moduslam.utils.auxiliary_methods import str_to_int


def read_binary(file: Path) -> tuple[float, ...]:
    """Reads binary data from a file.

    Args:
        file: path to the binary file.

    Returns:
        data: binary data as floats.
    """
    with open(file, "rb") as f:
        data = np.fromfile(f, np.float32)
        return tuple(data)


def get_csv_message_by_location(location: CsvDataLocation) -> Message:
    """Gets csv message by location.

    Args:
        location: location of the csv data.

    Returns:
        message: a message with csv data.
    """
    file = location.file
    num_lines = location.position
    with open(file, "r") as f:
        for _ in range(num_lines):
            line = next(f)
        message = get_csv_message(line, separator=",")
    return message


def get_pointcloud_message_by_location(location: BinaryDataLocation) -> Message:
    """Gets binary data by location.

    Args:
        location: location of the binary data.

    Returns:
        message: a message with binary data.
    """
    file = location.file
    data = read_binary(file)
    timestamp = file.stem
    return Message(timestamp, data)


def get_stereo_message_by_location(location: StereoImagesLocation) -> Message:
    """Get stereo images by location.

    Args:
        location: location of the stereo images.

    Returns:
        message: a message containing the stereo images.
    """
    left_image_file, right_image_file = location.files[0], location.files[1]
    timestamp_left, _ = left_image_file.stem, right_image_file.stem
    images = get_images(left_image_file, right_image_file)
    message = Message(timestamp_left, images)
    return message


def process_csv_line(row: list[str]):
    """Processes a row of a csv file and returns the timestamp, sensor name and index.

    Args:
        row: a row of a csv file.
    """
    timestamp = str_to_int(row[0])
    sensor_name = row[1]
    return timestamp, sensor_name


def create_sequence(
    file: Path, regime: TimeLimit | Stream, used_sensors: set[str]
) -> tuple[list[tuple[int, str, int]], dict[str, int]]:
    """Create a list of tuples containing the timestamp, sensor name and index.

    Args:
        file: csv file path.

        regime: a TimeLimit or Stream.

        used_sensors: a set of sensor names to be used.

    Returns:
        elements: a list of tuples containing the timestamp, sensor name and index.

        sensor_indices: a dictionary of sensor name and index pairs.
    """
    if isinstance(regime, TimeLimit):
        start = int(regime.start)
        stop = int(regime.stop)
        elements, latest_sensors_indices = process_timelimit(file, used_sensors, start, stop)
    else:
        elements, latest_sensors_indices = process_stream(file, used_sensors)

    if len(elements) == 0:
        latest_sensors_indices = {}

    return elements, latest_sensors_indices


def process_stream(
    file: Path, used_sensors: set[str]
) -> tuple[list[tuple[int, str, int]], dict[str, int]]:
    """Creates a list of tuples containing the timestamp, sensor name and index for the
    Stream regime.

    Args:
        file: csv file path.

        used_sensors: a set of sensor names to be used.

    Returns:
        elements: a list of tuples containing the timestamp, sensor name and index.

        latest_sensors_indices: a dictionary of sensor name and index pairs.
    """
    elements: list[tuple[int, str, int]] = []
    sensors_indices: dict[str, int] = {}
    latest_sensors_indices: dict[str, int] = {}
    default_index: int = 0

    for line in read_csv_file(file):
        timestamp, sensor_name = process_csv_line(line)
        index = sensors_indices.get(sensor_name, default_index) + 1
        sensors_indices[sensor_name] = index

        if sensor_name in used_sensors:
            latest_sensors_indices[sensor_name] = default_index
            elements.append((timestamp, sensor_name, index))

    return elements, latest_sensors_indices


def process_timelimit(
    file: Path, used_sensors: set[str], start: int, stop: int
) -> tuple[list[tuple[int, str, int]], dict[str, int]]:
    """Creates a list of tuples containing the timestamp, sensor name and index.

    Args:
        file: csv file path.

        used_sensors: a set of sensor names to be used.

        start: start timestamp.

        stop: stop timestamp.

    Returns:
        elements: a list of tuples containing the timestamp, sensor name and index.

        latest_sensors_indices: a dictionary of sensor name and index pairs.
    """
    elements: list[tuple[int, str, int]] = []
    sensors_indices: dict[str, int] = {}
    latest_sensors_indices: dict[str, int] = {}
    default_index: int = 0

    for line in read_csv_file(file):
        timestamp, sensor_name = process_csv_line(line)
        index = sensors_indices.get(sensor_name, default_index) + 1
        sensors_indices[sensor_name] = index

        if sensor_name not in used_sensors:
            continue

        else:
            if timestamp < start:
                latest_sensors_indices[sensor_name] = index

            if start <= timestamp <= stop:
                elements.append((timestamp, sensor_name, index))
                if sensor_name not in latest_sensors_indices:
                    latest_sensors_indices[sensor_name] = default_index

    return elements, latest_sensors_indices
