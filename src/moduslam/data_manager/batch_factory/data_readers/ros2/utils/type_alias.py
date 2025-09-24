"""Type alias for ROS-2 data reader based on rosbags.rosbag2.Reader."""

from collections.abc import Generator
from typing import TypeAlias

from rosbags.interfaces import Connection

Message: TypeAlias = tuple[Connection, int, bytes]
RosbagsMessageGenerator: TypeAlias = Generator[Message, None, None]
