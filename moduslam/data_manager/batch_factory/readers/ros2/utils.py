from collections.abc import Callable
from pathlib import Path

import pandas as pd
from rosbags.rosbag2 import Reader, Writer
from rosbags.serde import deserialize_cdr
from tabulate import tabulate

from moduslam.data_manager.batch_factory.readers.ros2.measurement_collector import (
    get_imu_measurement,
    get_lidar_measurement,
    get_stereo_measurement,
)


def get_rosbag_sensors(rosbag_path: Path):
    """Gets sensors and topics from a rosbag file.

    Args:
        Path: a path to the rosbag file.

    Returns:
        topics: a list of sensors in a dict.

    """
    sensors = []

    with Reader(rosbag_path) as reader:
        for connection in reader.connections:
            sensor_name = connection.topic.split("/")[1]
            data_type = connection.msgtype.split("/")[-1]
            sensor = {
                "id": connection.id,
                "topic": connection.topic,
                "message_type": connection.msgtype,
                "sensor": sensor_name,
                "data_type": data_type,
            }
            sensors.append(sensor)

    return sensors


def get_connections(topics: str | list[str], rosbag_path: Path) -> list | None:
    """Gets connections from a rosbag file.

    Args:
        topics: a string or a list of strings with topics names.

    Returns:
        connections: a list of connections.
    """
    topics_list = topics if isinstance(topics, list) else [topics]

    with Reader(rosbag_path) as reader:
        connections = [c for c in reader.connections if c.topic in topics_list]

        if len(connections) == 0:
            print(f"No connections found for topics: {topics_list}")
            return None
    return connections


def map_sensors(sensors: dict, sensor_list: list):
    """Maps sensors to topics.

    Args:
        sensors: a dictionary with the sensors in the ros2 Config

        topics: a list of topics from the Rosbags

    Returns:
        sensors_list: a list of sensors with each sensor parameters
    """
    updated_list = []
    connections_list = []
    sensor_types = ["Image", "PointCloud2", "Imu"]

    for sensor_params in sensor_list:
        for config_name, sensor_name in sensors.items():
            if (
                sensor_params["sensor"] == sensor_name
                and sensor_params["data_type"] in sensor_types
            ):
                sensor_params["sensor_name"] = config_name
                updated_list.append(sensor_params)
                connections_list.append(sensor_params["topic"])
                continue

    return connections_list, updated_list


def rosbag_iterator(reader, sensors, connections, time_range=None):
    """Iterates through the Readings of a Rosbag file based on the connections provided and returns data of each reading

    Args:
        reader: Rosbag reader object
        sensors: List of sensors in the moduslam configs.
        connections: List of connections for the sensors
    """

    data_getter: dict[str, Callable]
    data_getter = {
        "Imu": get_imu_measurement,
        "PointCloud2": get_lidar_measurement,
        "Image": get_stereo_measurement,
    }

    for i, (connection, timestamp, rawdata) in enumerate(reader.messages(connections=connections)):

        if time_range is not None:
            if timestamp < time_range.start:
                continue
            elif timestamp > time_range.stop:
                break
        sensor_name = "no sensor"
        sensor_id = connection.id
        sensor_topic = connection.topic.split("/")[1]
        data_type = connection.msgtype.split("/")[-1]

        if data_type not in data_getter.keys():
            continue

        msg = deserialize_cdr(rawdata, connection.msgtype)

        for single_sensor in sensors:
            if single_sensor["sensor"] == sensor_topic:
                sensor_name = single_sensor["sensor_name"]
                break

        message_getter = data_getter[data_type]
        data = message_getter(msg)

        yield (i, timestamp, sensor_name, data, data_type)


def rosbag_read(
    bag_path: Path, num_readings: int = 1, topic_name: str | None = None, print_table: bool = False
) -> list:
    """Reads a rosbag file and shows a determined number of readings in a table format.

    Args:
        bag_path: a path to the rosbag file.

        num_readings: the number of sensor readings to display in a table.

        topic_name: the topic name to read from the rosbag file.

    Returns:
        data: a list of tuples with the data from the rosbag file.
    """

    if print_table:
        table = [["ID", "ROS Topic", "Message Type", "Frame ID", "Message Count", "Timestamp"]]

    else:
        table = []

    with Reader(bag_path) as reader:
        if topic_name == None:
            connections = [c for c in reader.connections]

        else:
            connections = [c for c in reader.connections if c.topic == topic_name]

        for i, (connection, timestamp, rawdata) in enumerate(reader.messages()):

            if i <= num_readings:
                msg = deserialize_cdr(rawdata, connection.msgtype)

                row = [
                    i,
                    connection.topic,
                    connection.msgtype,
                    msg.header.frame_id,
                    connection.msgcount,
                    timestamp,
                    msg,
                ]
                table.append(row)
            else:
                if print_table:
                    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
                return table

        if print_table:
            print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))

    return table


def rosbag_write(bag_path: Path, new_path: Path, num_msgs: int = 1) -> None:
    """Writes a rosbag file with a specific number of sensor readings.

    Args:
        bag_path: a path to the rosbag file.

        new_path: a path to the new rosbag file.

        num_msgs: the number of messages to write.

    """

    # TODO: Remove prints and give more detailed information about bag paths.

    with Reader(bag_path) as reader:
        with Writer(new_path) as writer:

            rosbag_connections = []

            for connection in reader.connections:
                rosbag_connections.append(
                    writer.add_connection(connection.topic, connection.msgtype)
                )

            print(rosbag_connections)

            for i, (connection, timestamp, rawdata) in enumerate(reader.messages()):
                if i < num_msgs:
                    for c in rosbag_connections:
                        if connection.topic == c.topic:
                            writer.write(c, timestamp, rawdata)
                else:
                    print("Sucessfully writter {} messages in the new rosbag".format(i))
                    break


def get_csv_from_rosbag(rosbag_path: Path, csv_path: Path) -> None:
    """Gets sensor readings from a rosbag file and saves it into a CSV file.

    Args:
        rosbag_path: a path to the rosbag file.

        csv_path: a path to the CSV file.

    Returns:
        data: a list of tuples with the data from the rosbag file.
    """

    columns = ["ID", "ROS Topic", "Message Type", "Frame ID", "Message Count", "Timestamp"]
    rows = []
    with Reader(rosbag_path) as reader:
        for i, (connection, timestamp, rawdata) in enumerate(reader.messages()):

            msg = deserialize_cdr(rawdata, connection.msgtype)
            row = {
                "ID": i,
                "ROS Topic": connection.topic,
                "Message Type": connection.msgtype,
                "Frame ID": msg.header.frame_id,
                "Message Count": connection.msgcount,
                "Timestamp": timestamp,
            }

            rows.append(row)

    pd_df = pd.DataFrame(rows, columns=columns)

    pd_df.to_csv(csv_path, index=False)


def _create_csv(readings_lenght=15):
    print("Creating ROS2 test bags for the Ros2 Datareader ")

    DATA_PATH = "/home/felipezero/Projects/mySLAM_data/20231102_kia/"
    rosbag_name = "test_rosbag_" + str(readings_lenght)

    rosbag_path = Path(DATA_PATH, rosbag_name)
    csv_path = Path(DATA_PATH, rosbag_name + ".csv")

    get_csv_from_rosbag(rosbag_path=rosbag_path, csv_path=csv_path)


def _create_rosbag(num_readings=15):
    DATA_PATH = "/home/felipezero/Projects/mySLAM_data/20231102_kia/"
    rosbag_name = "rosbag2_2023_11_02-12_18_16"
    rosbag_path = Path(DATA_PATH, rosbag_name)

    new_rosbag_name = "test_rosbag_" + str(num_readings)

    rosbag_write(
        bag_path=rosbag_path, new_path=Path(DATA_PATH, new_rosbag_name), num_msgs=num_readings
    )

    rosbag_read(bag_path=Path(DATA_PATH, new_rosbag_name), num_readings=num_readings)


if __name__ == "__main__":
    _create_rosbag(15)
