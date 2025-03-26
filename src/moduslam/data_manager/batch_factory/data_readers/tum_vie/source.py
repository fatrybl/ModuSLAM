from pathlib import Path
from typing import TextIO

from src.moduslam.data_manager.batch_factory.data_readers.data_sources import (
    CsvData,
    StereoImageData,
)
from src.utils.exceptions import ClosedSourceError


class TumVieCsvData(CsvData):
    """CSV data source."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def open(self) -> None:
        """Opens the file and skips the header."""
        self._reset()
        self._source = open(self._file, "r")
        next(self._source)  # Skip header


class TumVieStereoImageData(StereoImageData):
    """Source of stereo images data."""

    def __init__(
        self,
        timestamp_file: Path,
        left_images_dir: Path,
        right_images_dir: Path,
        file_extension: str,
    ) -> None:
        super().__init__(left_images_dir, right_images_dir, file_extension)
        self._timestamp_file = timestamp_file
        self._timestamps: TextIO | None = None

    def __next__(self) -> tuple[Path, Path, str]:
        if self._timestamps is None:
            raise ClosedSourceError("Timestamp file is closed")
        left_image = next(self._left_images)
        right_image = next(self._right_images)
        line = next(self._timestamps)
        timestamp = line.split()[0]
        return left_image, right_image, timestamp

    def open(self) -> None:
        """Opens file with timestamps and skips header."""
        self._reset()
        self._timestamps = open(self._timestamp_file, "r")
        next(self._timestamps)  # Skip header

    def close(self) -> None:
        """Closes file with timestamps and resets directory iterators."""
        self._reset()
        if self._timestamps is not None:
            self._timestamps.close()
