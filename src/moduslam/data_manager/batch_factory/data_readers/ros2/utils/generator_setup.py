from collections.abc import Iterable

from rosbags.interfaces import Connection
from rosbags.rosbag2 import Reader

from src.moduslam.data_manager.batch_factory.data_readers.ros2.utils.type_alias import (
    RosbagsMessageGenerator,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit


def get_next_right_timestamp(
    reader: Reader, connections: Iterable[Connection], start: int, stop: int
) -> int:
    """Gets the next timestamp in the dataset.

    Args:
        reader: a reader to get the next timestamp from.

        connections: connections to use for messages.

        start: a timestamp to start from.

        stop: a timestamp to get the next timestamp for.

    Returns:
        next timestamp in the dataset.
    """
    next_timestamp = stop

    with reader:
        messages_gen = reader.messages(connections, start)

        for _, t, _ in messages_gen:
            if t > next_timestamp:
                next_timestamp = t
                break

    return next_timestamp


def setup_messages_gen(
    regime: Stream | TimeLimit,
    reader: Reader,
    connections: Iterable[Connection],
    end_timestamp: int,
) -> RosbagsMessageGenerator:
    """Sets up the generator for all messages.

    Args:
        regime: a data reader regime.

        reader: a reader to set up message generator for.

        connections: connections to set up message generator for.

        end_timestamp: a timestamp of the last message in the bag.

    Returns:
        messages generator.
    """
    if isinstance(regime, TimeLimit):
        start, stop = int(regime.start), int(regime.stop)

        if stop == end_timestamp:
            messages_gen = reader.messages(connections, start)

        else:
            stop = get_next_right_timestamp(reader, connections, start, stop)
            messages_gen = reader.messages(connections, start, stop)

    else:
        messages_gen = reader.messages(connections)

    return messages_gen
