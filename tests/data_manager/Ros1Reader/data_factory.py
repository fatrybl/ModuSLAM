from yaml import safe_dump
from pathlib import Path
from enum import Enum

from rosbags.rosbag1 import Writer
from rosbags.typesys.types import sensor_msgs__msg__NavSatFix, \
                                sensor_msgs__msg__NavSatStatus, \
                                std_msgs__msg__Header, builtin_interfaces__msg__Time,\
                                geometry_msgs__msg__Vector3, geometry_msgs__msg__Quaternion, \
                                sensor_msgs__msg__Imu
from rosbags.serde import serialize_ros1
from numpy import array
from slam.data_manager.factory.readers.ros1.ros1_reader import RosConfig
from configs.paths.DEFAULT_FILE_PATHS import RosDatasetStructure



class Sensor(Enum):
    IMU = 1,
    CAMERA = 2,
    LIDAR = 3, 
    GNSS = 4



def get_default_config() ->RosConfig:
    return RosConfig(topic_sensor_cfg = {"imu": TestDataFactory.IMU_TOPIC, "camera": TestDataFactory.CAMERA_TOPIC, "lidar": TestDataFactory.LIDAR_TOPIC, "gps": TestDataFactory.GNSS_TOPIC}, 
                                            sensors= ["imu", "camera", "lidar", "gps"], 
                                            deserialize_raw_data= False, 
                                            master_file_dir= TestDataFactory.MASTER_BAG_DIR)
class TestDataFactory:

    MASTER_BAG_DIR = Path(__file__).parent
    DEFAULT_CONFIG_PATH = Path(__file__).parent / "data_readers.yaml"

    MASTER_FILE_PATH = MASTER_BAG_DIR/RosDatasetStructure.master_filename.value
    DATA_PATH_FOLDER = MASTER_BAG_DIR/RosDatasetStructure.data_files_folder.value
    DATA_PATH_FOLDER.mkdir(parents=True, exist_ok=True)
    
    FILE1 = DATA_PATH_FOLDER/'test1.bag'
    FILE2= DATA_PATH_FOLDER/'test2.bag'
    FILE3 = DATA_PATH_FOLDER/'test3.bag'

    IMU_TOPIC, IMU_MSG = '/imu_topic', 'sensor_msgs/msg/Imu'
    CAMERA_TOPIC, CAMERA_MSG = '/camera_topic', 'sensor_msgs/msg/Image'
    LIDAR_TOPIC, LIDAR_MSG = '/lidar_topic', 'sensor_msgs/msg/LaserScan'
    GNSS_TOPIC, GNSS_MSG = '/gnss_topic', 'sensor_msgs/msg/NavSatFix'

    GNSS_POSITION  = [1.0, 2.0, 3.0]
    IMU_DATA = [1.11, 1.12, 1.13]


    
    def prepare_data(self):
        latitude, longitude, altitude = self.GNSS_POSITION
        msg = sensor_msgs__msg__NavSatFix(header = std_msgs__msg__Header(stamp=builtin_interfaces__msg__Time(sec=1314117928, nanosec=475285578, __msgtype__='builtin_interfaces/msg/Time'), frame_id = '/base_imu'),
                                                    status=sensor_msgs__msg__NavSatStatus(status=-1, service=1, STATUS_NO_FIX=-1, STATUS_FIX=0, STATUS_SBAS_FIX=1, STATUS_GBAS_FIX=2, SERVICE_GPS=1, SERVICE_GLONASS=2, SERVICE_COMPASS=4, SERVICE_GALILEO=8, __msgtype__='sensor_msgs/msg/NavSatStatus'),
                                                    latitude = latitude,
                                                    longitude = longitude,
                                                    altitude = altitude,
                                                    position_covariance= array([1., 1., 0., 0., 0., 0., 0., 0., 0.]),
                                                    position_covariance_type = 8)
        bin_data_gnss = serialize_ros1(msg, self.GNSS_MSG).tobytes()
        x, y, z, w = -0.2, -0.1, -0.712658166885376, 0.7014162540435791
        w_x, w_y, w_z = self.IMU_DATA
        msg = sensor_msgs__msg__Imu(header = std_msgs__msg__Header(stamp=builtin_interfaces__msg__Time(sec=1314117928, nanosec=475285578, __msgtype__='builtin_interfaces/msg/Time'), frame_id = '/base_imu'),
                                                        orientation= geometry_msgs__msg__Quaternion(x=-x, y=-y, z=-z, w=w, __msgtype__='geometry_msgs/msg/Quaternion'),
                                                        orientation_covariance=array([0., 0., 0., 0., 0., 0., 0., 0., 0.]), 
                                                        angular_velocity=geometry_msgs__msg__Vector3(x=w_x, y=w_y, z=w_z, __msgtype__='geometry_msgs/msg/Vector3'), 
                                                        angular_velocity_covariance=array([0., 0., 0., 0., 0., 0., 0., 0., 0.]),
                                                        linear_acceleration=geometry_msgs__msg__Vector3(x=-0.03592101112008095, y=0.03489848971366882, z=9.7805757522583, __msgtype__='geometry_msgs/msg/Vector3'), 
                                                        linear_acceleration_covariance=array([0., 0., 0., 0., 0., 0., 0., 0., 0.]))
        bin_data_imu = serialize_ros1(msg, self.IMU_MSG).tobytes()

        data_file1  = (self.FILE1,
                     [(Sensor.IMU, 2, b'123456789ABCDEQGEGKJBNKJBN'),
                      (Sensor.LIDAR, 3, b'DEADSFEEF'),
                      (Sensor.CAMERA, 4, b'JFVNKJGJHK'),
                      (Sensor.GNSS, 5, b'lugjgkjllk'),
                      (Sensor.IMU, 6, b'LKMLK2'),
                      (Sensor.LIDAR, 7, b'LKMLK2'),
                      (Sensor.CAMERA, 8, b'12345'),
                      (Sensor.GNSS, 9, bin_data_gnss)
                      ])
        
        data_file2  = (self.FILE2,
                        [(Sensor.IMU, 11, b'jkghbnkmigi'),
                        (Sensor.LIDAR, 12, b'78iguhbkjnknk'),
                        (Sensor.CAMERA, 13, b'yjg6t7lkj'),
                        (Sensor.GNSS, 14, b'iubgkhnlkml'),
                        (Sensor.IMU, 15, bin_data_imu),
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
        sensor_topic_dict ={Sensor.IMU: (self.IMU_TOPIC, self.IMU_MSG),
                            Sensor.CAMERA: (self.CAMERA_TOPIC, self.CAMERA_MSG),
                            Sensor.LIDAR:(self.LIDAR_TOPIC, self.LIDAR_MSG),
                            Sensor.GNSS:(self.GNSS_TOPIC, self.GNSS_MSG)}
        
       ### save bag files to masterfile
        with open(self.MASTER_FILE_PATH.name, 'w') as f:
            for file_path, data in DATA:
                f.write(file_path.name + '\n')
                with Writer(file_path) as writer:
                    used_conn = dict()
                    for sensor, timestamp, bin_data in data:
                        if(sensor not in used_conn):
                            topic, msg = sensor_topic_dict[sensor]
                            used_conn[sensor] = writer.add_connection(topic, msg, 'some message description')
                        writer.write(used_conn[sensor], timestamp, bin_data)
