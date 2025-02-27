import logging
from collections.abc import Callable
from pathlib import Path

import pandas as pd
from rosbags.rosbag2 import Reader, Writer
from rosbags.serde import deserialize_cdr

from moduslam.logger.logging_config import data_manager
from .data_getters import data_getter

logger = logging.getLogger(data_manager)
from collections import defaultdict
import heapq
from rosbags.rosbag2 import Reader

class MergedSensorIterator:
    """
    Iterates through the readings of a Rosbag file based on the provided connections
    and returns data of each reading in a merged, sorted order.

    Args:
        sensor_iterators: Dictionary of sensor iterators.

    Returns:
        Tuple[int, str, any]: Timestamp, sensor name, and data.
    """
    def __init__(self, sensor_iterators):
        self.messages = []

        # Collect all messages into one list
        for sensor, iterator in sensor_iterators.items():
            for timestamp, rawdata in iterator.messages:
                self.messages.append((timestamp, sensor, rawdata))

        self.messages.sort(key=lambda x: x[0])
        self.index = 0  # Index for iteration

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.messages):
            raise StopIteration
        message = self.messages[self.index]
        self.index += 1
        return message  # (timestamp, sensor, rawdata)

class TimeRangeSensorIterator:
    """
    Iterator for sensor messages filtered by a specific time range.

    Args:
        messages: List of tuples containing (timestamp, data).
        start_time: Start of the time range.
        end_time: End of the time range.

    Returns:
        Tuple[int, any]: Timestamp and data within the given range.
    """
    def __init__(self, messages, start_time, end_time):
        # Filter messages by the given time range
        self.messages = [m for m in messages if start_time <= m[0] <= end_time]
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.messages):
            entry = self.messages[self.index]
            self.index += 1
            return entry
        raise StopIteration

class SensorIterator:
    """
    Iterator for sensor messages in stream mode.

    Args:
        messages: List of tuples containing (timestamp, data).

    Returns:
        Tuple[int, any]: Timestamp and data.
    """
    def __init__(self, messages):
        # Sort messages by timestamp (first element of each tuple)
        self.messages = sorted(messages, key=lambda x: x[0])
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.messages):
            entry = self.messages[self.index]
            self.index += 1
            return entry
        raise StopIteration

def read_rosbag(bag_path, topics_table: dict[str, str], mode="stream", start_time=None, end_time=None):
    """
    Reads a Rosbag file and returns sensor data iterators based on the selected mode.

    Args:
        bag_path: Path to the Rosbag file.
        topics_table: Dictionary mapping sensor names to topics.
        mode: Processing mode ('stream' or 'time_range').
        start_time (optional): Start time for 'time_range' mode.
        end_time (optional): End time for 'time_range' mode.

    Returns:
        MergedSensorIterator: An iterator over all sensor messages.
    """
    sensor_data = {}  # key is sensor name, value is message list
    valid_topics = set(topics_table.values())

    with Reader(bag_path) as reader:
        for connection, timestamp, rawdata in reader.messages():
            sensor_name = connection.topic  # Define the sensor name
            if sensor_name in valid_topics:
                if sensor_name not in sensor_data:
                    sensor_data[sensor_name] = []
                sensor_data[sensor_name].append((timestamp, rawdata))

    # For each sensor we create our own iterator
    if mode == "stream":
        sensor_iterators = {}
        for sensor, messages in sensor_data.items():
            print(f"Creating iterator for sensor: {sensor} with {len(messages)} messages")
            for i, msg in enumerate(messages, start=1):  # нумерация
                print(f"  Message {i}: Timestamp: {msg[0]}")
            sensor_iterators[sensor] = SensorIterator(messages)

    elif mode == "time_range":
        if start_time is None or end_time is None:
            raise ValueError("start_time and end_time must be provided for time_range mode")
        sensor_iterators = {
            sensor: TimeRangeSensorIterator(messages, start_time, end_time)
            for sensor, messages in sensor_data.items()
        }
    else:
        raise ValueError("Invalid mode")

    merged_iterator = MergedSensorIterator(sensor_iterators)
    print("\nMerged and sorted sensor messages:")
    for timestamp, sensor, rawdata in merged_iterator:
        print(f"Timestamp: {timestamp}, Sensor: {sensor}")

    return merged_iterator  # Возвращает итератор


def get_rosbag_sensors(rosbag_path: Path, sensors_table: dict[str, str], topics_table: dict[str, str]) -> list[dict[str, str]]:
    sensors = []

    with Reader(rosbag_path) as reader:
        for connection in reader.connections:
            sensor_topic = connection.topic
            for sensor, topic_path in topics_table.items():
                # print(f"Checking topic: {sensor_topic} against {topic_path}")
                if sensor_topic == topic_path:
                    # print(f"Topic match found for {sensor}: {topic_path}")

                    # ищем соответствующее значение в sensors_table
                    # Ищем по значению, а не по ключу
                    # print(f"Looking for matching sensor in sensors_table...")
                    for key, value in sensors_table.items():
                        print(f"Checking sensor: {key} with value {value}")
                        if value == sensor:  # Если значение в sensors_table совпадает с найденным ключом
                            # sensors.append({"sensor": key})
                            sensors.append({"sensor_name": key, "sensor_type": value})
                            print(f"Added sensor: {key} (from sensors_table)")
                            break  # После добавления элемента не продолжаем искать
                    else:
                        print(f"Sensor with value {sensor} not found in sensors_table")
                    break  # Не ищем дальше, если нашли соответствие
    print("Final list of added sensors:")
    for sensor in sensors:
        print(sensor)
    return sensors
    # структура {'sensor_name': 'sensor_type'}

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

# def get_connections(topics: str | list[str], rosbag_path: Path) -> list | None:
#     """Gets connections from a rosbag file. This will extract only the sensor data from
#     specific sensor topics.
#
#     Args:
#         topics: a string or a list of strings with topics names.
#
#     Returns:
#         connections: a list of connections.
#     """
#     topics_list = topics if isinstance(topics, list) else [topics]
#
#     with Reader(rosbag_path) as reader:
#         connections = [c for c in reader.connections if c.topic in topics_list]
#
#         if len(connections) == 0:
#             print(f"No connections found for topics: {topics_list}")
#             return None
#     return connections

def rosbag_iterator(reader, sensors, connections, time_range=None):
    """Iterates through the Readings of a Rosbag file based on the connections provided
    and returns data of each reading.

    Args:
        reader: Rosbag reader object.
        sensors: List of sensors in the moduslam configs.
        connections: List of connections for the sensors.
        time_range (optional): Time range to filter messages.

    Yields:
        Tuple[int, float, str, any]: Index, timestamp, sensor name, data.
    """
    sensors_dict = {sensor["sensor_name"]: sensor["sensor_type"] for sensor in sensors}

    for i, (connection, timestamp, rawdata) in enumerate(reader.messages(connections=connections)):

        if time_range is not None and not (time_range.start <= timestamp <= time_range.stop):
            continue

        sensor_topic = connection.topic.split("/")[1]
        # print("------------------------------------")
        # print("sensor_topic", sensor_topic)
        data_type = connection.msgtype.split("/")[-1]
        # print("------------------------------------")
        # print("data_type", data_type)
        # print("------------------------------------")
        # message_type = connection.msgtype
        # print("data_type", message_type)
        # print("------------------------------------")

        if data_type not in data_getter.keys():
            continue
        if sensor_topic not in sensors_dict:
            continue

        msg = deserialize_cdr(rawdata, connection.msgtype)
        data = data_getter[data_type](msg)
        print( f"Yielding: Index: {i}, Timestamp: {timestamp}, Sensor: {sensors_dict[sensor_topic]}, Data: {data}")

        yield (i, timestamp, sensors_dict[sensor_topic], data)

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


# def _rosbag_write(bag_path: Path, new_path: Path, num_msgs: int = 1) -> None:
#     """Writes a rosbag file with a specific number of sensor readings.
#
#     Args:
#         bag_path: a path to the rosbag file.
#
#         new_path: a path where to save the new rosbag file.
#
#         num_msgs: the total number of messages to be saved in the new rosbag file.
#     """
#
#     with Reader(bag_path) as reader:
#         with Writer(new_path) as writer:
#
#             rosbag_connections = []
#
#             for connection in reader.connections:
#                 rosbag_connections.append(
#                     writer.add_connection(connection.topic, connection.msgtype)
#                 )
#
#             print(rosbag_connections)
#
#             for i, (connection, timestamp, rawdata) in enumerate(reader.messages()):
#                 if i < num_msgs:
#                     for c in rosbag_connections:
#                         if connection.topic == c.topic:
#                             writer.write(c, timestamp, rawdata)
#                 else:
#                     print("Sucessfully writter {} messages in the new rosbag".format(i))
#                     break

#
# def _get_csv_from_rosbag(rosbag_path: Path, csv_path: Path) -> None:
#     """Gets all the sensor readings from a rosbag file and saves them into a CSV file.
#
#     Args:
#         rosbag_path: a path to the rosbag file.
#
#         csv_path: a path where to save the CSV file.
#     """
#
#     columns = ["ID", "ROS Topic", "Message Type", "Frame ID", "Message Count", "Timestamp"]
#     rows = []
#     with Reader(rosbag_path) as reader:
#         for i, (connection, timestamp, rawdata) in enumerate(reader.messages()):
#
#             msg = deserialize_cdr(rawdata, connection.msgtype)
#             row = {
#                 "ID": i,
#                 "ROS Topic": connection.topic,
#                 "Message Type": connection.msgtype,
#                 "Frame ID": msg.header.frame_id,
#                 "Message Count": connection.msgcount,
#                 "Timestamp": timestamp,
#             }
#
#             rows.append(row)
#
#     pd_df = pd.DataFrame(rows, columns=columns)
#
#     pd_df.to_csv(csv_path, index=False)


# def _create_csv(readings_lenght=15):
#     """Creates a CSV file from a rosbag file.
#
#     Args:
#         readings_lenght: the number of sensor readings to read from the rosbag and write to the CSV file.
#     """
#     print("Creating ROS2 test bags for the Ros2 Datareader ")
#
#     DATA_PATH = "/home/felipezero/Projects/mySLAM_data/20231102_kia/"
#     rosbag_name = "test_rosbag_" + str(readings_lenght)
#
#     rosbag_path = Path(DATA_PATH, rosbag_name)
#     csv_path = Path(DATA_PATH, rosbag_name + ".csv")
#
#     _get_csv_from_rosbag(rosbag_path=rosbag_path, csv_path=csv_path)
