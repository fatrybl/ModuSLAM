"""Iterates over files in a directory with a given extension.

TODO: add tests.
"""

import logging
from pathlib import Path

from moduslam.utils.auxiliary_methods import sort_files_numerically
from phd.logger.logging_config import data_manager

logger = logging.getLogger(data_manager)


class DirectoryIterator:

    _start_index = -1

    def __init__(self, directory: Path, file_extension: str):
        self._directory = directory
        self._extension = file_extension
        self._files: list[Path] = list(directory.glob(f"*{file_extension}"))
        self._files = sort_files_numerically(self._files)
        self._num_files: int = len(self._files)
        self._index: int = self._start_index

    def __iter__(self):
        return self

    def __next__(self) -> Path:
        if self._num_files == 0 or self._index == self._num_files - 1:
            raise StopIteration
        self._index += 1
        return self._files[self._index]

    @property
    def index(self) -> int:
        """Index of the current file.

        Raises:
            IndexError:
                1. if the directory is empty.
                2. if no iterations has been performed.
        """
        if self._is_empty():
            msg = f"No files of type{self._extension} in the directory."
            logger.error(msg)
            raise IndexError(msg)

        if self._index == self._start_index:
            msg = "Index does not exist: no iteration has been done yet."
            logger.error(msg)
            raise IndexError(msg)

        return self._index

    @property
    def file(self) -> Path:
        """Current file.

        Raises:
            FileExistsError: if no files of the specified type exist in the directory.

            ValueError: if no iteration has been performed yet.
        """
        if self._is_empty():
            msg = f"No files of type{self._extension} in the directory."
            logger.error(msg)
            raise FileExistsError(msg)
        try:
            file = self._files[self.index]
        except IndexError:
            msg = "No iteration has been done yet."
            logger.error(msg)
            raise ValueError(msg)

        return file

    def reset_index(self) -> None:
        """Resets the index to the initial state."""
        self._index = self._start_index

    def _is_empty(self) -> bool:
        """Checks if any files are present in the directory.

        Returns:
              check status.
        """
        return self._num_files == 0
