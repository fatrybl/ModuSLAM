import os
import time
from dataclasses import dataclass
from pathlib import Path

from rosbags.rosbag2 import Writer, Reader
from rosbags.serde import deserialize_cdr
from tabulate import tabulate


@dataclass
class RosbagsManager:
    bag_path: Path

    def rosbag_read(self, num_readings:int = 1) -> list:
        n = 1
        topics_list: list = []
        table = [["number","ROS Topic","Message type","Frame ID","Message count", "Timestamp"]]
        with Reader(self.bag_path) as reader:
            print("The following topics exist in the actual rosbag file")
            for connection in reader.connections:
                # print(f" topic: {connection.topic} and type: {connection.msgtype}")
                topics_list.append(connection.topic)

            for connection, timestamp, rawdata in reader.messages():
                if n <= num_readings:
                    msg = deserialize_cdr(rawdata, connection.msgtype)
                    dt_obj = int(str(timestamp)[0:10])
                    nano_seconds = int(str(timestamp)[10:])
                    # print(dt_obj, nano_seconds)
                    row = [n,connection.topic,connection.msgtype,msg.header.frame_id,connection.msgcount, timestamp]
                    table.append(row)
                    n += 1

                else:
                    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
                    return topics_list, table

            return topics_list, table


    def rosbag_write(self, new_path: Path = '', msg_limit: int = 1):
        with Reader(self.bag_path) as reader:
            with Writer(new_path) as writer:
                n = 1
                connections = []

                for connection in reader.connections:
                        connections.append(writer.add_connection(connection.topic, connection.msgtype))

                for connection, timestamp, rawdata in reader.messages():
                    if n <= msg_limit:
                        for c in connections:
                            if connection.topic == c.topic:
                                writer.write(c, timestamp, rawdata)
                        n += 1
                    else:
                        print("Sucessfully written {} messages in the new rosbag2".format(n-1))

                        break

    def sensor_manager(self, bag_path: Path, num_readings: int = -1):
        pass

if __name__ == "__main__":

    now_time = int(time.time())
    folder_path = Path(os.environ['DATA_DIR'])
    bag_path = Path('{}/rosbag2_2023_11_02-12_18_16'.format(folder_path))
    new_bag_path = Path('{0}/rosbag2_2024_{1:2d}'.format(folder_path, now_time))


    rb_manager = RosbagsManager(bag_path)   

    # rb_manager.rosbag_write(new_bag_path, msg_limit=100)

    rb_manager2 = RosbagsManager(new_bag_path)
    messages: list = rb_manager2.rosbag_read(num_readings=10)


