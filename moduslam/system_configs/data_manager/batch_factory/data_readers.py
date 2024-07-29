"""Unique identifiers for the data readers."""

from dataclasses import dataclass


@dataclass
class DataReaders:
    kaist_reader: str = "Kaist Reader"
    tum_vie_reader: str = "Tum Vie Reader"
    ros2_reader: str = "Ros2 Reader"
