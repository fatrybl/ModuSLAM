"""Tests for Ros2Reader constructor.

1) test_ros2_reader_1: Successful creation. 2) test_ros2_reader_2: Successful creation.
creation and exploration of rosbag 3) test_ros2_reader_3: Unsuccessful creation with
non-existent directory
"""

from pathlib import Path

import pytest

from moduslam.data_manager.batch_factory.readers.ros2.reader import Ros2DataReader
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream, TimeLimit
from tests.conftest import ros2_dataset_dir

from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensor_factory import SensorsFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.setup_manager.sensors_factory.sensors import Imu

def test_reader_initialization_with_single_sensor():
    sensor_config = SensorConfig(name="stereo", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})
    SensorsFactory.init_sensors(factory_config)

    dataset_cfg = Ros2Config(directory=ros2_dataset_dir, sensors_table={"stereo": "sensor_info"})
    reader = Ros2DataReader(regime=Stream(), dataset_params=dataset_cfg)
    assert reader is not None

def test_reader_initialization_with_multiple_sensors():
    sensor_config_1 = SensorConfig(name="stereo", type_name=Sensor.__name__)
    sensor_config_2 = SensorConfig(name="lidar", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={
        sensor_config_1.name: sensor_config_1,
        sensor_config_2.name: sensor_config_2
    })
    SensorsFactory.init_sensors(factory_config)

    dataset_cfg = Ros2Config(
        directory=ros2_dataset_dir,
        sensors_table={"stereo": "sensor_info", "lidar": "sensor_info"}
    )
    reader = Ros2DataReader(regime=Stream(), dataset_params=dataset_cfg)
    assert reader is not None

def test_reader_initialization_with_invalid_dataset_path():
    dataset_cfg = Ros2Config(directory=Path("some/invalid/dataset/path"))
    with pytest.raises(NotADirectoryError):
        Ros2DataReader(regime=Stream(), dataset_params=dataset_cfg)

def test_reader_with_valid_time_limit():
    sensor_config = SensorConfig(name="stereo", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})
    SensorsFactory.init_sensors(factory_config)
    dataset_cfg = Ros2Config(directory=ros2_dataset_dir, sensors_table={"stereo": "sensor_info"})
    reader = Ros2DataReader(regime=TimeLimit(1698927496694033807, 1698927497190095250), dataset_params=dataset_cfg)
    assert reader is not None

def test_reader_with_start_timestamp_greater_than_stop():
    sensor_config = SensorConfig(name="stereo", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})
    SensorsFactory.init_sensors(factory_config)

    dataset_cfg = Ros2Config(directory=ros2_dataset_dir, sensors_table={"stereo": "sensor_info"})
    with pytest.raises(ValueError, match="timestamp start.*can not be greater than stop"):
        Ros2DataReader(
            regime=TimeLimit(1698927497190095250, 1698927496694033807),
            dataset_params=dataset_cfg,
        )

def test_reader_with_negative_start_timestamp():
    sensor_config = SensorConfig(name="stereo", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})
    SensorsFactory.init_sensors(factory_config)

    dataset_cfg = Ros2Config(directory=ros2_dataset_dir, sensors_table={"stereo": "sensor_info"})
    with pytest.raises(ValueError, match="timestamp start=.*can not be negative"):
        Ros2DataReader(
            regime=TimeLimit(-1698927496694033807, 1698927497190095250),
            dataset_params=dataset_cfg,
        )

def test_reader_with_valid_short_time_range():
    sensor_config = SensorConfig(name="stereo", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})
    SensorsFactory.init_sensors(factory_config)

    dataset_cfg = Ros2Config(directory=ros2_dataset_dir, sensors_table={"stereo": "sensor_info"})
    reader = Ros2DataReader(regime=TimeLimit(0, 5000), dataset_params=dataset_cfg)
    assert reader is not None





