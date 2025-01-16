import logging
from collections.abc import Callable
from pathlib import Path

import pandas as pd
from rosbags.rosbag2 import Reader, Writer
from rosbags.serde import deserialize_cdr

from moduslam.data_manager.batch_factory.readers.ros2.measurement_collector import (
    get_imu_measurement,
    get_lidar_measurement,
    get_stereo_measurement,
)
from moduslam.logger.logging_config import data_manager

logger = logging.getLogger(data_manager)


def get_rosbag_sensors(rosbag_path: Path, sensors_table: dict[str, str], topics_table: dict[str, str]) -> list[dict[str, str]]:
    """Gets sensors and topics from a ROS bag file.

    Args:
        rosbag_path (Path): Path to the ROS bag file.
        sensors_table (dict[str, str]): Mapping of sensor names to their corresponding topic names.
        topics_table (dict[str, str]): Mapping of sensor names to their full topic paths.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing metadata for each sensor.
    """
    sensors = []

    with Reader(rosbag_path) as reader:
        for connection in reader.connections:
            parts = connection.topic.split("/")
            sensor_name = parts[1] if len(parts) > 1 else connection.topic
            sensor_topic = connection.topic
            # print(sensor_topic)
            data_type = connection.msgtype.split("/")[-1]
            if sensor_name not in sensors_table or sensor_topic not in topics_table.values():
                continue

            sensor = {
                "id": connection.id,
                "topic": connection.topic,
                "message_type": connection.msgtype,
                "sensor_name": sensor_name,
                "data_type": data_type,
                "sensor": sensors_table[sensor_name],
            }
            sensors.append(sensor)

    return sensors


def check_setup_sensors(dataset_manager_sensors: dict, setup_manager_sensors: set) -> dict:
    """Checks and compares the sensors in the setup_manager and the sensors available in
    the rosbag.

    If the sensor is not found in the sensors table, it raises an error. Then, the table
    is updated with the sensor name from the setup_manager. .
    """
    sensor_names = list(dataset_manager_sensors.keys())
    new_sensors_table = {}

    for sensor in setup_manager_sensors:
        if sensor.name not in sensor_names:
            logger.error(f"Sensor {sensor.name} not found in the sensors table")
            raise ValueError(f"Sensor {sensor.name} not found in the Datamanager's sensors table")
        else:
            new_sensors_table[dataset_manager_sensors[sensor.name]] = sensor.name

    return new_sensors_table


def get_connections(topics: str | list[str], rosbag_path: Path) -> list | None:
    """Gets connections from a rosbag file. This will extract only the sensor data from
    specific sensor topics.

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


def rosbag_iterator(reader, sensors, connections, time_range=None):
    """Iterates through the Readings of a Rosbag file based on the connections provided
    and returns data of each reading.

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
        sensor_topic = connection.topic.split("/")[1]
        data_type = connection.msgtype.split("/")[-1]

        if data_type not in data_getter.keys():
            continue

        msg = deserialize_cdr(rawdata, connection.msgtype)

        for single_sensor in sensors:
            if single_sensor["sensor_name"] == sensor_topic:
                sensor_name = single_sensor["sensor"]
                break

        if sensor_name == "no sensor":
            continue

        message_getter = data_getter[data_type]
        data = message_getter(msg)

        yield (i, timestamp, sensor_name, data, data_type)


def rosbag_read(bag_path: Path, num_readings: float = 1) -> list:
    """Reads a rosbag file and returns a list with the sensor readings.

    Args:
        bag_path: a path to the rosbag file.

        num_readings: the number of sensor readings to store in the list.

    Returns:
        data: a list of list with the data from the rosbag file.
    """

    table = []

    with Reader(bag_path) as reader:

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
                return table
    return table


def _rosbag_write(bag_path: Path, new_path: Path, num_msgs: int = 1) -> None:
    """Writes a rosbag file with a specific number of sensor readings.

    Args:
        bag_path: a path to the rosbag file.

        new_path: a path where to save the new rosbag file.

        num_msgs: the total number of messages to be saved in the new rosbag file.
    """

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


def _get_csv_from_rosbag(rosbag_path: Path, csv_path: Path) -> None:
    """Gets all the sensor readings from a rosbag file and saves them into a CSV file.

    Args:
        rosbag_path: a path to the rosbag file.

        csv_path: a path where to save the CSV file.
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
    """Creates a CSV file from a rosbag file.

    Args:
        readings_lenght: the number of sensor readings to read from the rosbag and write to the CSV file.
    """
    print("Creating ROS2 test bags for the Ros2 Datareader ")

    DATA_PATH = "/home/felipezero/Projects/mySLAM_data/20231102_kia/"
    rosbag_name = "test_rosbag_" + str(readings_lenght)

    rosbag_path = Path(DATA_PATH, rosbag_name)
    csv_path = Path(DATA_PATH, rosbag_name + ".csv")

    _get_csv_from_rosbag(rosbag_path=rosbag_path, csv_path=csv_path)
