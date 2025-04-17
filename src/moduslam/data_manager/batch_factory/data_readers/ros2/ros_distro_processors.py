from typing import Any, Protocol

from rosbags.typesys import Stores

from src.moduslam.data_manager.batch_factory.data_readers.ros2.msg_processors.s3e_dataset.type_method_table import (
    table,
)


class MessageProcessor(Protocol):
    """Interface for messages processor for any ROS-2 distribution."""

    def process(self, msg: object, msg_type: str) -> Any:
        """Processes a ROS-2 message and returns a measurement.

        Args:
            msg: ROS message.

            msg_type: ROS message type.

        Returns:
            a measurement.
        """


class Ros2Humble(MessageProcessor):
    """Messages processor for ROS-2 Jazzy."""

    def __init__(self):
        self._table = table

    def process(self, msg: object, msg_type: str) -> Any:
        """Processes a ROS message and returns a measurement.

        Args:
            msg: ROS message.

            msg_type: ROS message type.

        Returns:
            a measurement.
        """
        processor = self._table[msg_type]
        data = processor(msg)
        return data


def get_msg_processor(type_store: Stores) -> MessageProcessor:
    """Gets the message processor for a specific ROS-2 distribution.

    Args:
        type_store: a ROS-2 distro type store to use.

    Returns:
        a message processor.

    Raises:
        NotImplementedError: if the message processor is not implemented for the given type store.
    """
    match type_store:

        case Stores.ROS2_HUMBLE:
            return Ros2Humble()

        case _:
            raise NotImplementedError(f"Message processor for {type_store} is not implemented")
