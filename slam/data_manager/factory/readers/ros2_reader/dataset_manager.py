import os
from pathlib import Path

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import DatasetConfig


class DatasetManager(DatasetConfig):

    def __init__(self, dataset_path:Path, name:str="", url:str="", reader:str="Rosbag2 reader"):
        super().__init__(name=name, url=url, directory=dataset_path, reader=reader)
        self.sensors: dict = {'Camera':['left', 'right'], 'Lidar':['vlp16r','vlp16l', 'vlp32c', 'merger'], 'Imu':['xsens']}

        self.dataset_path:Path = dataset_path
        self.topics:list = []
        self.sensors_list = []
        self.raw_data:list = []

    def read_dataset(self, num_readings:int = -1):
        """
        Read a set amount of data read from a rosbags2 file and stores them in a local variable
        :param num_readings: number of readings from the rosbags2 to take
        :return: List of sensors found inside of the rosbags2 file
        """
        n = 1
        with Reader(self.dataset_path) as reader:
            for connection in reader.connections:
                self.topics.append(connection.topic)
                for sensor in self.sensors.keys():
                    if(connection.topic.split('/')[1] in self.sensors[sensor]):
                        self.sensors_list.append(sensor)

            if num_readings == -1:
                for connection, timestamp, rawdata in reader.messages():
                        msg = deserialize_cdr(rawdata, connection.msgtype)
                        dt_obj = int(str(timestamp)[0:10])
                        nano_seconds = int(str(timestamp)[10:])
                        # print(dt_obj, nano_seconds)
                        row = [
                            n,
                            connection.topic,
                            connection.msgtype,
                            msg.header.frame_id,
                            connection.msgcount,
                            timestamp,
                            msg,
                        ]
                        n += 1
                        self.raw_data.append(row)

                print(f"{n-1} data readings extracted from the file")

            elif num_readings > 0:
                for connection, timestamp, rawdata in reader.messages():
                    if n <= num_readings:
                        msg = deserialize_cdr(rawdata, connection.msgtype)
                        dt_obj = int(str(timestamp)[0:10])
                        nano_seconds = int(str(timestamp)[10:])
                        # print(dt_obj, nano_seconds)
                        row = [
                            n,
                            connection.topic,
                            connection.msgtype,
                            msg.header.frame_id,
                            connection.msgcount,
                            timestamp,
                            msg,
                        ]
                        self.raw_data.append(row)
                        n += 1

                    else:
                        print(f"{n-1} data readings extracted from the file")
                        break

                print(f"{n-1} data readings extracted from the file")

            else:
                print("Error")

    def get_data_list(self) -> list:
        return self.raw_data

    def organize_data(self, sensors: str | list = "all") -> list:
        data_list = []
        if sensors == 'all':
            print("Getting all data")
            for data in self.raw_data:
                new_dict = self.convert_2_dict(data)
                data_list.append(new_dict)

            return data_list


        elif type(sensors) is str:
            print(f"Getting only {sensors} data")
            for data in self.raw_data:
                if data[1].split('/')[1] in self.sensors[sensors]:
                    new_dict = self.convert_2_dict(data)
                    data_list.append(new_dict)
            return data_list


        elif type(sensors) is list:
            print(f"Getting only {sensors} data")
            for data in self.raw_data:
                for sensor in sensors:
                    if data[1].split('/')[1] in self.sensors[sensor]:
                        new_dict = self.convert_2_dict(data)
                        data_list.append(new_dict)

            return data_list


        else:
            print(f"{sensors} was not found in the list of sensors")


    def convert_2_dict(self, data):

        message_dict = {'Position':list(), 'Timestamp':list()}
        topic_dict = {'Topic':'', 'Message Type':'','Frame ID':'','Message count':0, 'Message':{}}
        sensor_dict = {'Sensor':'', 'Topics':{}}


        for sensor_name, sensor_list in self.sensors.items():
            if data[1].split('/')[1] in sensor_list:

                message_dict['Position'].append(data[0])
                message_dict['Timestamp'].append(data[5])

                topic_dict['Topic'] = data[2]
                topic_dict['Message Type'] = data[2].split('/')[-1]
                topic_dict['Frame ID'] = data[3]
                topic_dict['Message count'] = int(data[4])
                topic_dict['Message'] = message_dict

                sensor_dict['Sensor'] = sensor_name
                sensor_dict['Topics'] = topic_dict

        return sensor_dict



if __name__ == "__main__":

    print("Testing DatasetManager")
    folder_path = Path(os.environ["DATA_DIR"])
    bag_path = Path("{}/rosbag2_2024_1713944720".format(folder_path))
    ds_manager = DatasetManager(bag_path)

    ds_manager.read_dataset(200)
    my_sensors = ["Camera"]
    my_data = ds_manager.organize_data(my_sensors)

    n = 0
    for data in my_data:
        n += 1
        print(data)

    print(f"Total of {n} observations")