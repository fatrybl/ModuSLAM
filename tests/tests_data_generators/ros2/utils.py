from collections.abc import Iterable
from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.typesys.store import Typestore

from moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from moduslam.data_manager.batch_factory.data_readers.locations import (
    Ros2DataLocation,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.ros_distro_processors import (
    MessageProcessor,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.utils.type_alias import (
    Message,
)
from moduslam.sensors_factory.sensors import Sensor


def read_messages(path: Path) -> list[Message]:
    """Reads messages from ROS-2 dataset.

    Args:
        path: path to the dataset.

    Returns:
        list of tuples: connection, timestamp, and raw data.
    """
    data: list[Message] = []

    with Reader(path) as reader:
        for connection, timestamp, rawdata in reader.messages():
            data.append((connection, timestamp, rawdata))

    return data


def create_elements(
    messages: Iterable[Message],
    topic_sensor_map: dict[str, Sensor],
    msg_processor: MessageProcessor,
    type_store: Typestore,
) -> list[Element]:
    """Creates elements from messages.

    Args:
        messages: ROS-2 messages.

        topic_sensor_map: mapping between topic names and sensors.

        msg_processor: processor of raw ROS-2 messages

        type_store: ROS-2 type store from rosbags lib.

    Returns:
        elements.
    """

    elements: list[Element] = []

    for connection, timestamp, raw_data in messages:
        msg = type_store.deserialize_cdr(raw_data, connection.msgtype)
        processed_data = msg_processor.process(msg, connection.msgtype)

        sensor = topic_sensor_map[connection.topic]
        measurement = RawMeasurement(sensor, processed_data)
        location = Ros2DataLocation(connection.topic)

        elements.append(Element(timestamp, measurement, location))

    return elements
