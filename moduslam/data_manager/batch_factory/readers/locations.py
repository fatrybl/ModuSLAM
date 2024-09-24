"""Locations of different data sources.

Defines the location of a data batch element.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, eq=True)
class Location:
    """Base location.

    Use for inheritance.
    """


@dataclass(frozen=True, eq=True)
class ConfigFileLocation(Location):
    file: Path


@dataclass(frozen=True, eq=True)
class BinaryDataLocation(Location):
    """The location of binary data file."""

    file: Path


@dataclass(frozen=True, eq=True)
class StereoImagesLocation(Location):
    """The location of stereo images."""

    files: tuple[Path, Path] = field(metadata={"unit": "image path"})


@dataclass(frozen=True, eq=True)
class CsvDataLocation(Location):
    """The location of .csv file and the position (line number) in it."""

    file: Path
    position: int


@dataclass(frozen=True, eq=True)
class TxtDataLocation(CsvDataLocation):
    """The location of .txt file and the position (line number) in it."""


@dataclass(frozen=True, eq=True)
class RosbagLocation(Location):
    """The location of a rosbag file and the position (index) in it."""

    file: Path
    position: int
