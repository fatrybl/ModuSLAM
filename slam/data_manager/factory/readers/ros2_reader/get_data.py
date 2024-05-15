import os
from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr


class DataGrabber():
    
    _data:list = []

    @classmethod
    def iter_rosbag(self, bagpath:Path, position:int)->list:
        n=0
        with Reader(bagpath) as reader:
            for connection, timestamp, rawdata in reader.messages():
                    if n == position:
                        msg = deserialize_cdr(rawdata, connection.msgtype)
                        dt_obj = int(str(timestamp)[0:10])
                        nano_seconds = int(str(timestamp)[10:])
                        # print(dt_obj, nano_seconds)
                        _data = [
                            n,
                            connection.topic,
                            connection.msgtype,
                            msg.header.frame_id,
                            connection.msgcount,
                            timestamp,
                            msg
                        ]
                        # print(_data)
                        return _data, timestamp
                    n += 1
            return None

if __name__ == "__main__":
    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2024_1713944720".format(folder_path))
    DataGrabber.iter_rosbag(bag_path, 30)