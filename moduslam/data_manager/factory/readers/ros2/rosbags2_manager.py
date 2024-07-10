import os
import time
from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

from moduslam.data_manager.factory.readers.ros2.data_iterator import Iterator
from moduslam.utils.auxiliary_dataclasses import TimeRange


class Rosbags2Manager:

    def __init__(self, bag_path, sensors_table, time_range: TimeRange = None):
        self.bag_path: Path = bag_path
        self.iterator = Iterator()
        self.sensors: dict = sensors_table
        self.sensors_list = self._map_sensors()
        if time_range is not None:
            self.start = time_range.start
            self.stop = time_range.stop

        else:
            self.start = -1
            self.stop = -1

        print(f"Rosbag2 Manager initialized with the following sensors:\n{self.sensors_list}")

        # table = self.rosbag_read(num_readings=20)

    def _get_topics(self):
        sensor: dict = {}
        sensors = []

        with Reader(self.bag_path) as reader:

            for connection in reader.connections:
                sensor_name = connection.topic.split("/")[1]
                data_type = connection.msgtype.split("/")[-1]
                sensor = {
                    "id": connection.id,
                    "topic": connection.topic,
                    "message_type": connection.msgtype,
                    "sensor_name": sensor_name,
                    "data_type": data_type,
                }
                sensors.append(sensor)
        return sensors

    def _map_sensors(self):
        print("Mapping topics to sensors")
        sensors_list = self._get_topics()
        for k, v in self.sensors.items():
            for sensor in sensors_list:
                if sensor["sensor_name"] in v:
                    sensor["sensor_type"] = k

        return sensors_list

    def rosbag_read(self, num_readings: int = 1, topic_name: str = None) -> list:

        n = 1
        with Reader(self.bag_path) as reader:
            if topic_name == None:
                connections = [c for c in reader.connections]
            else:
                connections = [c for c in reader.connections if c.topic == topic_name]

            for connection, timestamp, rawdata in reader.messages(connections=connections):
                print(f"Reading messages from {self.start} to {self.stop}")
                if n == num_readings:
                    msg = deserialize_cdr(rawdata, connection.msgtype)
                    dt_obj = int(str(timestamp)[0:10])
                    nano_seconds = int(str(timestamp)[10:])
                    # print(dt_obj, nano_seconds)
                    data = [
                        connection.id,
                        connection.topic,
                        connection.msgtype,
                        msg.header.frame_id,
                        timestamp,
                        msg,
                    ]

                    n += 1

                else:
                    return data
            return data

    def next_sensor_read(self):
        n = 1

        with Reader(self.bag_path) as reader:
            for connection, timestamp, rawdata in reader.messages():
                if n == self.iterator.get_iter():
                    if timestamp < self.start:
                        print(f"timestamp {timestamp} is not yet in {self.start}")
                        n += 1
                        self.iterator.next()
                        continue
                    elif timestamp > self.stop:
                        print(f"reached the stop timestamp {self.stop}")
                        return None

                    msg = deserialize_cdr(rawdata, connection.msgtype)
                    dt_obj = int(str(timestamp)[0:10])
                    nano_seconds = int(str(timestamp)[10:])
                    # print(dt_obj, nano_seconds)
                    data = (n, connection.id, connection.topic, connection.msgtype, timestamp)
                    data = (connection.id, n, msg, timestamp)
                    self.iterator.next()
                    return data
                else:
                    n += 1
            return None


if __name__ == "__main__":

    now_time = int(time.time())
    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2023_11_02-12_18_16".format(folder_path))
    new_bag_path = Path("{0}/rosbag2_2024_{1:2d}".format(folder_path, now_time))

    rb_manager = Rosbags2Manager(bag_path)

    # rb_manager.rosbag_write(new_bag_path, msg_limit=100)

    rb_manager2 = Rosbags2Manager(new_bag_path)
    messages: list = rb_manager2.rosbag_read(num_readings=10)
