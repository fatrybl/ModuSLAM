"""Tests for Ros2Reader constructor.

1) test_ros2_reader_1: Successful creation.
2) test_ros2_reader_2: Successful creation.
creation and exploration of rosbag
3) test_ros2_reader_3: Unsuccessful
creation with non-existent directory
"""

from pathlib import Path

import pytest

from moduslam.data_manager.batch_factory.readers.ros2.reader import Ros2DataReader
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import Stream
from tests.conftest import ros2_dataset_dir


def test_ros2_reader_1():
    print(ros2_dataset_dir)
    dataset_cfg = Ros2Config(directory=ros2_dataset_dir)
    reader = Ros2DataReader(regime=Stream(), dataset_params=dataset_cfg)
    assert reader is not None


def test_ros2_reader_2():
    dataset_cfg = Ros2Config(directory=ros2_dataset_dir)
    limit_check = 20
    rosbag_reader = Ros2DataReader(regime=Stream(), dataset_params=dataset_cfg)
    with rosbag_reader as reader:

        print("Rosbag opened successfully")

    print("Rosbag closed successfully")


def test_ros2_reader_3():
    dataset_cfg = Ros2Config(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(NotADirectoryError):
        Ros2DataReader(regime=Stream(), dataset_params=dataset_cfg)
