"""A module to create a test bag for any ROS 2 dataset."""

from rosbags.interfaces import Connection
from rosbags.rosbag2 import Reader, Writer
from rosbags.typesys import Stores, get_typestore
from rosbags.typesys.store import Typestore


def split_ros2_bag(
    input_bag_path: str, output_bag_path: str, n_messages: int, typestore: Typestore
):
    """Creates a ROS-2 bag with first N messages of the input bag.

    Args:
        input_bag_path: path to input ROS 2 bag

        output_bag_path: path to output ROS 2 bag

        n_messages: Number of messages to copy per topic

        typestore: ROS 2 distribution specific typestore from rosbags lib.
    """
    topic_connection_map: dict[str, Connection] = {}

    with Reader(input_bag_path) as reader, Writer(output_bag_path, version=9) as writer:
        messages = reader.messages()

        if reader.message_count < n_messages:
            raise ValueError(
                f"Not enough messages. Only {reader.message_count} messages available."
            )

        for con in reader.connections:
            writer.add_connection(topic=con.topic_name, msgtype=con.msgtype, typestore=typestore)

        for con in writer.connections:
            topic_connection_map[con.topic] = con

        for _ in range(n_messages):
            connection, timestamp, rawdata = next(messages)
            con = topic_connection_map[connection.topic]
            writer.write(con, timestamp, rawdata)


if __name__ == "__main__":
    typestore = get_typestore(Stores.LATEST)

    # Use absolute paths to the input and output bag files
    split_ros2_bag(
        input_bag_path="/home/mark/Downloads/s3e_dataset",
        output_bag_path="/home/mark/Desktop/PhD/ModuSLAM/src/tests_data/datasets/ros2/s3e_playground_2",
        n_messages=20,
        typestore=typestore,
    )
