from pathlib import Path

from pytest import raises
from rosbags.typesys import Stores

from moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2Config,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.reader import Ros2Reader
from moduslam.utils.exceptions import DataReaderConfigurationError
from tests.conftest import s3e_dataset_dir


def test_successful_creation():
    dataset_cfg = Ros2Config(directory=s3e_dataset_dir, ros_distro=Stores.ROS2_HUMBLE)
    reader = Ros2Reader(dataset_params=dataset_cfg)
    assert reader is not None


def test_invalid_dataset_directory():
    dataset_cfg = Ros2Config(
        directory=Path("some/invalid/dataset/path"), ros_distro=Stores.ROS2_HUMBLE
    )

    with raises(DataReaderConfigurationError):
        Ros2Reader(dataset_params=dataset_cfg)


def test_invalid_ros2_distro():
    dataset_cfg = Ros2Config(directory=s3e_dataset_dir, ros_distro="invalid_distro")  # type: ignore

    with raises(DataReaderConfigurationError):
        Ros2Reader(dataset_params=dataset_cfg)
