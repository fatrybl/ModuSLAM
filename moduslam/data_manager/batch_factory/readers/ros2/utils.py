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

        # Собираем все сообщения от каждого сенсора в общий список
        for sensor, iterator in sensor_iterators.items():
            for timestamp, rawdata in iterator.messages:
                self.messages.append((timestamp, sensor, rawdata))

        # Сортируем список по временным меткам
        self.messages.sort(key=lambda x: x[0])

        # После сортировки назначаем глобальный индекс
        self.messages = [
            (idx, timestamp, sensor, rawdata)
            for idx, (timestamp, sensor, rawdata) in enumerate(self.messages)
        ]

        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.messages):
            raise StopIteration
        result = self.messages[self.index]
        self.index += 1
        return result  # (global_index, timestamp, sensor, rawdata)


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
    sensor_data = {}  # ключ - имя сенсора, значение - список сообщений
    valid_topics = set(topics_table.values())

    with Reader(bag_path) as reader:
        for connection, timestamp, rawdata in reader.messages():
            # Ищем имя сенсора (например, imu) по имени топика (/xsens/imu/data)
            sensor_name = next(
                (sensor for sensor, topic in topics_table.items() if topic == connection.topic),
                None
            )

            if sensor_name is None:
                continue

            if sensor_name not in sensor_data:
                sensor_data[sensor_name] = []
            sensor_data[sensor_name].append((timestamp, rawdata))

    if mode == "stream":
        sensor_iterators = {}
        for sensor, messages in sensor_data.items():
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

    # Создаём общий итератор со всеми сообщениями
    merged_iterator = MergedSensorIterator(sensor_iterators)

    return merged_iterator

