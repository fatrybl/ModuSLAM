import logging
from collections.abc import Iterator
from csv import DictReader, reader
from dataclasses import dataclass, field
from pathlib import Path

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.utils.exceptions import FileNotValid

logger = logging.getLogger(__name__)


@dataclass
class FileIterator:
    """Iterator for the sensor`s timestamp file."""

    file: Path
    position: int = 0
    iterator: Iterator = field(init=False)

    def __post_init__(self):
        if DataReader.is_file_valid(self.file):
            f = open(self.file, "r")
            self.iterator = reader(f)
        else:
            msg = f"File {self.file} is not valid."
            logger.critical(msg)
            raise FileNotValid

    def __next__(self):
        try:
            values = next(self.iterator)
            self.position += 1
            return values
        except StopIteration:
            raise

    def __iter__(self):
        return self.iterator

    def reset(self):
        """Reset the iterator to the beginning of the file."""
        self.position = 0
        self.__post_init__()


class CsvFileGenerator:
    """File generator to read each row of "data_stamp.csv" as a dictionary."""

    def __init__(self, file_path: Path, names: list[str]):
        """
        Args:
            file_path: path of the file.
            names: dictionary keys` names.
        """
        self.__file = open(file_path, "r")
        self.__reader = DictReader(self.__file, fieldnames=names)

    def __next__(self) -> dict[str, str]:
        try:
            val = next(self.__reader)
            return val
        except StopIteration:
            self.__file.close()
            raise

    def __iter__(self):
        return self
