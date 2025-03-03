"""Any data source.

TODO: add tests.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TextIO

from src.moduslam.data_manager.batch_factory.readers.directory_iterator import (
    DirectoryIterator,
)
from src.utils.exceptions import ClosedSourceError


class Source(ABC):
    @abstractmethod
    def __next__(self):
        """Returns the next data element."""

    @abstractmethod
    def open(self, *args, **kwargs) -> None:
        """Opens the source: initializes files, iterators, etc..."""

    @abstractmethod
    def close(self, *args, **kwargs) -> None:
        """Closes and resets the source."""


class CsvData(Source):
    """CSV data source."""

    def __init__(self, file_path: Path) -> None:
        self._file = file_path
        self._source: TextIO | None = None
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
        self._reset()

    def close(self) -> None:
        """Closes the file."""
        if self._source is not None:
            self._source.close()
            self._source = None
            self._reset()

    def _reset(self) -> None:
        self._index = 0


class PointCloudData(Source):
    """Source of point cloud data."""

    def __init__(self, directory_path: Path, file_extension: str) -> None:
        self._iter = DirectoryIterator(directory_path, file_extension)

    def __next__(self):
        data = next(self._iter)
        return data

    @property
    def file(self) -> Path:
        """Point cloud data file."""
        return self._iter.file

    def open(self) -> None:
        self._iter.reset_index()

    def close(self) -> None:
        """Resets directory iterator."""
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
        self._reset()

    def close(self) -> None:
        """Resets directory iterators."""
        self._reset()

    def _reset(self):
        self._left_images.reset_index()
        self._right_images.reset_index()
