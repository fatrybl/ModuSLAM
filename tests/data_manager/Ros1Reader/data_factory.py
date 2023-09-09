from yaml import dump
from pathlib import Path
from enum import Enum

from rosbags.rosbag1 import Writer

from configs.paths.DEFAULT_FILE_PATHS import RosDataset



def create_config_file(cfg: dict) -> None:
    with open(TestDataFactory.DEFAULT_CONFIG_PATH, 'w') as outfile:
        dump(cfg, outfile)


class Sensor(Enum):
    IMU = 1,
    CAMERA = 2,
    LIDAR = 3, 
    GNSS = 4

class TestDataFactory:
    MASTER_BAG_DIR = Path(__file__).parent
    DEFAULT_CONFIG_PATH = Path(__file__).parent / "data_readers.yaml"

    MASTER_FILE_PATH = MASTER_BAG_DIR/RosDataset.master_filename.value
    DATA_PATH_FILDER = MASTER_BAG_DIR/RosDataset.data_files_folder.value
    DATA_PATH_FILDER.mkdir(parents=True, exist_ok=True)
    
    FILE1 = DATA_PATH_FILDER/'test1.bag'
    FILE2= DATA_PATH_FILDER/'test2.bag'
    FILE3 = DATA_PATH_FILDER/'test3.bag'

    def prepare_data(self):
        IMU_TOPIC, IMU_MSG = '/imu_topic', 'sensor_msgs/msg/Imu'
        CAMERA_TOPIC, CAMERA_MSG = '/camera_topic', 'sensor_msgs/msg/Image'
        LIDAR_TOPIC, LIDAR_MSG = '/lidar_topic', 'sensor_msgs/msg/LaserScan'
        GNSS_TOPIC, GNSS_MSG = '/gnss_topic', 'sensor_msgs/msg/NavSatFix'

        data_file1  = (self.FILE1,
                     [(Sensor.IMU, 1, b'123456789ABCDEQGEGKJBNKJBN'),
                      (Sensor.LIDAR, 2, b'DEADSFEEF'),
                      (Sensor.CAMERA, 3, b'JFVNKJGJHK'),
                      (Sensor.GNSS, 4, b'lugjgkjllk'),
                      (Sensor.IMU, 5, b'LKMLK2'),
                      (Sensor.LIDAR, 6, b'LKMLK2'),
                      (Sensor.CAMERA, 7, b'12345'),
                      (Sensor.GNSS, 8, b'kjnk987')
                      ])
        
        data_file2  = (self.FILE2,
                        [(Sensor.IMU, 11, b'jkghbnkmigi'),
                        (Sensor.LIDAR, 12, b'78iguhbkjnknk'),
                        (Sensor.CAMERA, 13, b'yjg6t7lkj'),
                        (Sensor.GNSS, 14, b'iubgkhnlkml'),
                        (Sensor.IMU, 15, b'kjhkuyhjlk'),
                        (Sensor.LIDAR, 16, b'i7tftgvbjh'),
                        (Sensor.CAMERA, 17, b'97657567tyu'),
                        (Sensor.GNSS, 18, b'kjbkjfygk')
                        ])
        
        data_file3  = (self.FILE3,
                        [(Sensor.IMU, 21, b'JHBNKJ<K'),
                        (Sensor.LIDAR, 22, b'JHKIKL'),
                        (Sensor.CAMERA, 23, b'KJHKJ'),
                        (Sensor.GNSS, 24, b'KUHJL')])
        
        DATA =  [data_file1, data_file2, data_file3]
        sensor_topic_dict ={Sensor.IMU: (IMU_TOPIC, IMU_MSG),
                            Sensor.CAMERA: (CAMERA_TOPIC, CAMERA_MSG),
                            Sensor.LIDAR:(LIDAR_TOPIC, LIDAR_MSG),
                            Sensor.GNSS:(GNSS_TOPIC, GNSS_MSG)}
        
       ### save bag files to masterfile
        with open(self.MASTER_FILE_PATH.name, 'w') as f:
            for file_path, data in DATA:
                f.write(file_path.name + '\n')
                with Writer(file_path) as writer:
                    used_conn = dict()
                    for sensor, timestamp, bin_data in data:
                        if(sensor not in used_conn):
                            topic, msg = sensor_topic_dict[sensor]
                            used_conn[sensor] = writer.add_connection(topic, msg, 'MESSAGE_DEFINITION')
                        writer.write(used_conn[sensor], timestamp, bin_data)
