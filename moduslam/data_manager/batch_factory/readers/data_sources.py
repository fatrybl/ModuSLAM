"""Any data source.

TODO: add tests.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TextIO

from moduslam.data_manager.batch_factory.readers.directory_iterator import (
    DirectoryIterator,
)
from moduslam.utils.exceptions import ClosedSourceError


class Source(ABC):
    @abstractmethod
    def __next__(self):
        """Returns the next data element.

        Raises:
            StopIteration: If the source is exhausted.
        """

    def open(self) -> None:
        """Opens the source: initializes files, iterators, etc..."""

    def flush(self) -> None:
        """Flushes the source: closes files, resets iterators, etc..."""


class CsvData(Source):
    """CSV data source."""

    def __init__(self, file_path: Path) -> None:
        self._source: TextIO | None = None
        self._file = file_path
        self._index: int = 0

    def __next__(self):
        if self._source is None:
            msg = "The source is closed. Please call open() before calling next()."
            raise ClosedSourceError(msg)
        data = next(self._source)
        self._index += 1
        return data

    @property
    def file(self) -> Path:
        """CSV data file."""
        return self._file

    @property
    def position(self) -> int:
        """Current position in the file."""
        return self._index

    def open(self) -> None:
        """Opens the file."""
        self._source = open(self._file, "r")

    def flush(self) -> None:
        """Closes the file."""
        if self._source is not None:
            self._source.close()
            self._source = None
            self._index = 0


class PointcloudData(Source):
    """Source of pointcloud data."""

    def __init__(self, directory_path: Path, file_extension: str) -> None:
        self._iter = DirectoryIterator(directory_path, file_extension)

    def __next__(self):
        data = next(self._iter)
        return data

    @property
    def file(self) -> Path:
        """Pointcloud data file."""
        return self._iter.file

    def open(self) -> None:
        """Opens the source."""
        self._iter.reset_index()


class StereoImageData(Source):
    """Source of stereo images data."""

    def __init__(self, left_images_dir: Path, right_images_dir: Path, file_extension: str) -> None:
        self._left_images = DirectoryIterator(left_images_dir, file_extension)
        self._right_images = DirectoryIterator(right_images_dir, file_extension)

    def __next__(self):
        left_image = next(self._left_images)
        right_image = next(self._right_images)
        return left_image, right_image

    @property
    def files(self) -> tuple[Path, Path]:
        """Stereo image files."""
        return self._left_images.file, self._right_images.file

    def open(self) -> None:
        """Opens the source."""
        self._left_images.reset_index()
        self._right_images.reset_index()
