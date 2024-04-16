import os
import time
from pathlib import Path

from rosbags.rosbag2 import Writer, Reader

now_time = int(time.time())

folder_path = Path(os.environ['DATA_DIR'])
bag_path = Path('{}/rosbag2_2023_11_02-12_18_16'.format(folder_path))
new_bag_path = Path('{0}/rosbag2_2024_{1:2d}'.format(folder_path, now_time))

print(new_bag_path)
messages_limit = 2000

with Reader(bag_path) as reader:
    with Writer(new_bag_path) as writer:
        n = 0
        connections = []

        for connection in reader.connections:
                print(f" topic: {connection.topic} and type: {connection.msgtype}")

                connections.append(writer.add_connection(connection.topic, connection.msgtype))

        print(connections)

        for connection, timestamp, rawdata in reader.messages():
            if n < messages_limit:
                for c in connections:
                    if connection.topic == c.topic:
                        writer.write(c, timestamp, rawdata)
                n += 1
            else:
                print("Sucessfully written {} messages in the new rosbag2".format(n))
                break
