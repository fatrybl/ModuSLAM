"""Tests for TumVieReader instance."""

from pathlib import Path

import pytest

from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.reader import (
    TumVieReader,
)
from src.moduslam.sensors_factory.configs import ImuConfig
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.tests.conftest import tum_vie_dataset_dir
from src.utils.exceptions import DataReaderConfigurationError


def test_tum_vie_reader_successful_creation():
    SensorsFactory.init_sensors({"imu": ImuConfig("imu")})
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    reader = TumVieReader(dataset_params=dataset_cfg)
    assert reader is not None


def test_tum_vie_reader_invalid_dataset_directory():
    dataset_cfg = TumVieConfig(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(DataReaderConfigurationError):
        TumVieReader(dataset_params=dataset_cfg)


def test_tum_vie_reader_invalid_data_file():
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    dataset_cfg.txt_files = {dataset_cfg.imu_name: Path("some/invalid/imu.file")}

    with pytest.raises(DataReaderConfigurationError):
        TumVieReader(dataset_params=dataset_cfg)
