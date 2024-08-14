from collections.abc import Callable
from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

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
    print(f"Getting connections for topics: {topics_list}")

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

    for sensor_params in sensor_list:
        for config_name, sensor_name in sensors.items():
            if sensor_params["sensor"] == sensor_name:
                sensor_params["sensor_name"] = config_name
                updated_list.append(sensor_params)
                connections_list.append(sensor_params["topic"])
                continue

    return connections_list, updated_list


def rosbag_iterator(reader, sensors, connections):
    """Iterates through the Readings of a Rosbag file based on the connections provided and returns data of each reading

    Args:
        reader: Rosbag reader object
        sensors: List of sensors in the moduslam configs.
        connections: List of connections for the sensors
    """

    for i, (connection, timestamp, rawdata) in enumerate(reader.messages(connections=connections)):
        sensor_name = "no sensor"
        sensor_id = connection.id
        sensor = connection.topic.split("/")[1]
        data_type = connection.msgtype.split("/")[-1]
        msg = deserialize_cdr(rawdata, connection.msgtype)

        for single_sensor in sensors:
            if single_sensor["sensor"] == sensor:
                sensor_name = single_sensor["sensor_name"]
                break

        # TODO: get the actual data from msg in the measurement_collector.py
        test_dict: dict[str, Callable]
        test_dict = {
            "imu": get_imu_measurement,
            "lidar": get_lidar_measurement,
            "stereo": get_stereo_measurement,
        }
        message_getter = test_dict[data_type]
        data = message_getter(msg)

        yield (i, timestamp, sensor_name, data, data_type)


def main():
    """Main function."""
    folder_path = Path(
        "/home/felipezero/Projects/mySLAM_data/20231102_kia/rosbag2_2023_11_02-12_18_16"
    )


if __name__ == "__main__":
    main()
