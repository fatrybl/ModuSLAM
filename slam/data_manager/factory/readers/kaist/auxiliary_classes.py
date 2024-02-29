import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from slam.data_manager.factory.element import Location

logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=True)
class Message:
    """Message with a timestamp and any data."""

    timestamp: str
    data: tuple[Any, ...]


@dataclass(frozen=True, eq=True)
class BinaryDataLocation(Location):
    """Binary data location."""

    file: Path


@dataclass(frozen=True, eq=True)
class StereoImgDataLocation(Location):
    """Stereo data location.

    Stores paths as a tuple.
    """

    files: tuple[Path, ...] = field(metadata={"unit": "images paths"})


@dataclass(frozen=True, eq=True)
class CsvDataLocation(Location):
    """
    Csv data location: a file and position (line number) in a file.
    """

    file: Path
    position: int
