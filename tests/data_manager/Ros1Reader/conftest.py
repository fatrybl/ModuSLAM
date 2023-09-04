from pytest import fixture
from yaml import dump
from shutil import rmtree, copyfile
from pathlib import Path

from rosbags.rosbag1 import Writer

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader

TEST_BAG_PATH = Path(__file__).parent/"test100.bag" 
DEFAULT_CONFIG_PATH = Path(__file__).parent / "data_readers.yaml"

def create_config_file(cfg: dict) -> None:
    with open(DEFAULT_CONFIG_PATH, 'w') as outfile:
        dump(cfg, outfile)

@fixture(scope='module', autouse=True)
def prepare_data():
    with Writer(TEST_BAG_PATH) as writer:
        conn_imu = writer.add_connection('/imu_topic', 'sensor_msgs/msg/Imu', 'MESSAGE_DEFINITION')
        conn_camera = writer.add_connection('/camera_topic', 'sensor_msgs/msg/Image', 'MESSAGE_DEFINITION')
        conn_lidar = writer.add_connection('/lidar_topic', 'sensor_msgs/msg/LaserScan', 'MESSAGE_DEFINITION')
        conn_gnss = writer.add_connection('/gnss_topic', 'sensor_msgs/msg/NavSatFix', 'MESSAGE_DEFINITION')
        
        writer.write(conn_imu, 1, b'123456789ABCDEQGEGKJBNKJBN')
        writer.write(conn_lidar, 2, b'DEADSFEEF')
        writer.write(conn_camera, 3, b'JFVNKJGJHK')
        writer.write(conn_gnss, 4, b'lugjgkjllk')
        writer.write(conn_imu, 5, b'LKMLK2')
        writer.write(conn_lidar, 6, b'LKMLK2')
        writer.write(conn_camera, 7, b'12345')
        writer.write(conn_gnss, 8, b'kjnk987')
    yield


@fixture(scope='module', autouse=True)
def clean():
    yield
    TEST_BAG_PATH.unlink()
    DEFAULT_CONFIG_PATH.unlink()

