from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr


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

    print(f"Updated sensors list: {updated_list}")
    print(f"Connections list: {connections_list}")

    return connections_list, updated_list


def rosbag_read(
    rosbag_path: Path, topic_name: str | list, reading_pos: int = 1
) -> dict[str, any] | None:
    """Reads a rosbag file.

    Args:
        topic_name: a string with the specific topic name of the wanted sensor readings.
        num_readings: an integer with the number of readings to be read.

    Returns:
        sensor: a dictionary with values of the requested sensor.
    """

    with Reader(rosbag_path) as reader:
        print(f"Reading messages from {topic_name} for {reading_pos} times.")
        connections = [c for c in reader.connections if c.topic == topic_name]
        if len(connections) == 0:
            raise ValueError(f"Topic {topic_name} not found in the rosbag file.")
            return None

        for i, (connection, timestamp, rawdata) in enumerate(
            reader.messages(connections=connections)
        ):
            if i == reading_pos:
                msg = deserialize_cdr(rawdata, connection.msgtype)
                sensor_id = connection.id
                sensor_name = connection.topic.split("/")[1]
                data_type = connection.msgtype.split("/")[-1]
                sensor = {
                    "id": sensor_id,
                    "topic": connection.topic,
                    "message_type": connection.msgtype,
                    "sensor": sensor_name,
                    "data_type": data_type,
                    "message": msg,
                }

                return sensor
        return None


def main():
    """Main function."""
    folder_path = Path(
        "/home/felipezero/Projects/mySLAM_data/20231102_kia/rosbag2_2023_11_02-12_18_16"
    )
    sensors = get_rosbag_sensors(folder_path)
    for sensor in sensors:
        sensor_read = rosbag_read(folder_path, sensor["topic"], 1)
        if sensor_read is not None:
            for key, value in sensor_read.items():
                print(f"{key}: {value}")
            print(
                "---------------------------------------------------------------------------------------------------------"
            )

    sensor_config = {}


if __name__ == "__main__":
    main()
