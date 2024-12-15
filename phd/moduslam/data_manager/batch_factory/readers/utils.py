import csv
import logging
from collections.abc import Iterable, Iterator, Mapping, Sequence
from pathlib import Path

import PIL
from PIL.Image import Image

from phd.logger.logging_config import data_manager
from phd.moduslam.data_manager.batch_factory.readers.data_sources import Source
from phd.moduslam.utils.auxiliary_dataclasses import Message
from phd.moduslam.utils.exceptions import ExternalModuleException, ItemNotFoundError

logger = logging.getLogger(data_manager)


def set_state(
    sensor_name: str, timestamp: int, data_sequence: Sequence[tuple[int, str, int]], source: Source
) -> None:
    """Sets the iterator position for the given sensor and timestamp.

    Args:
        sensor_name: name of sensor to set the iterator position.

        timestamp: timestamp to set the iterator position.

        data_sequence: sequence of data.

        source: table of sensors and their sources.

    Raises:
        ItemNotFoundError: if no measurement found for the sensor at the given timestamp.

    TODO: add tests
    """
    for t, name, position in data_sequence:
        if t == timestamp and name == sensor_name:
            for _ in range(position - 1):
                next(source)
            return

    msg = (
        f"Can not set the initial state for sensor {sensor_name} at {timestamp}. "
        f"No measurement has been found."
    )
    logger.error(msg)
    raise ItemNotFoundError(msg)


def read_csv_file(file_path: Path, delimiter: str = ",") -> Iterator[list[str]]:
    """Read a csv file and yield each row.

    Args:
        file_path: path to the csv file.

        delimiter: line objects delimiter.

    Yields:
        a row of the csv file.
    """
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            yield row


def is_file_valid(file_path: Path) -> bool:
    """Checks if the file is valid: exists and not empty.

    Args:
        file_path: path to the file.

    Returns:
        validity status.
    """
    if not file_path.is_file():
        msg = f"The path is not a file-path: {file_path!r}"
        logger.critical(msg)
        return False
    elif file_path.stat().st_size == 0:
        msg = f"File {file_path!r} is empty."
        logger.critical(msg)
        return False
    else:
        return True


def check_files(files: Iterable[Path]) -> None:
    """Checks if the files exist.

    Args:
        files: collection of files.

    Raises:
        FileNotFoundError: if any path does not correspond to file.
    """
    for f in files:
        if not f.is_file():
            msg = f"File {f!r} does not exist."
            logger.critical(msg)
            raise FileNotFoundError(msg)


def check_directory(directory_path: Path) -> None:
    """Checks if a directory exists for the given path.

    Args:
        directory_path: path to the directory.

    Raises:
        NotADirectoryError: if the path is not a directory path or the directory does not exist.
    """
    if not directory_path.exists() or not directory_path.is_dir():
        msg = f"The path {directory_path!r} either does not exist or is not a directory"
        logger.error(msg)
        raise NotADirectoryError(msg)


def get_csv_message(line: str, separator: str = " ") -> Message:
    """Gets csv message.

    Args:
        line: a string with data.

        separator: string separator.

    Returns:
        message: a message with csv data.
    """
    line = line.strip()
    data = line.split(sep=separator)
    timestamp = data[0]
    values = tuple(data[1:])
    return Message(timestamp, values)


def get_image(file_path: Path) -> Image:
    """Gets the image from the given path.

    Args:
        file_path: file with the image.

    Returns:
        PIL image.

    Raises:
        ExternalModuleException: PIL.Image failed to read an image.
    """
    try:
        image = PIL.Image.open(file_path)
        return image
    except (FileNotFoundError, PermissionError, PIL.UnidentifiedImageError) as e:
        msg = f"PIL.image module failed to read: {file_path}. Error: {str(e)}"
        logger.critical(msg)
        raise ExternalModuleException(msg) from e


def get_images(left_image_file: Path, right_image_file) -> tuple[Image, Image]:
    """Gets stereo images.

    Args:
        left_image_file: left image file.

        right_image_file: right image file.

    Returns:
        message: a message with stereo images.
    """

    left_img = get_image(left_image_file)
    right_img = get_image(right_image_file)
    return left_img, right_img


def filter_table(table: Mapping[str, Source], sensors: set[str]) -> dict[str, Source]:
    """Filters "sensor <-> source" table by the given sensors.

    Args:
        table: a dictionary of "sensor name <-> source" pairs.

        sensors: a set of sensor names to be used.

    Returns:
        a filtered table.
    """
    filtered_table = {}
    for sensor_name, source in table.items():
        if sensor_name in sensors:
            filtered_table[sensor_name] = source
    return filtered_table


def apply_state(sensor_source_table: dict[str, Source], state: dict[str, int]) -> None:
    """Applies the latest state of the iterators for the sequential reading.

    Args:
        sensor_source_table: a dictionary of "sensor <-> source" pairs.

        state: a dictionary of current state for each sensor.
    """
    for sensor, source in sensor_source_table.items():
        num_steps = state[sensor]
        for _ in range(num_steps):
            next(source)
