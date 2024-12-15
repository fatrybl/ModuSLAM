"""Tests for TumVieReader constructor.

1) test_tum_vie_reader_1: Successful creation. 2) test_tum_vie_reader_2: Unsuccessful
creation with non-existent dataset directory. 3) test_tum_vie_reader_3: Unsuccessful
creation with non-existent data_stamp.csv file.
"""

from pathlib import Path

import pytest

from phd.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.setup_manager.sensors_factory.configs import ImuConfig
from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from phd.moduslam.utils.exceptions import DataReaderConfigurationError
from phd.tests.conftest import tum_vie_dataset_dir


def test_tum_vie_reader_successful_creation():
    SensorsFactory.init_sensors({"imu": ImuConfig("imu")})
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    reader = TumVieReader(regime=Stream(), dataset_params=dataset_cfg)
    assert reader is not None


def test_tum_vie_reader_invalid_dataset_directory():
    dataset_cfg = TumVieConfig(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(DataReaderConfigurationError):
        TumVieReader(regime=Stream(), dataset_params=dataset_cfg)


def test_tum_vie_reader_invalid_data_file():
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    dataset_cfg.csv_files = {dataset_cfg.imu_name: Path("some/invalid/imu.file")}

    with pytest.raises(DataReaderConfigurationError):
        TumVieReader(regime=Stream(), dataset_params=dataset_cfg)


def test_kaist_reader_sensors_regime_mismatch():
    SensorsFactory.clear()
    SensorsFactory.init_sensors({"imu": ImuConfig("imu")})
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    regime = TimeLimit(-1, 0)

    with pytest.raises(DataReaderConfigurationError):
        TumVieReader(regime, dataset_cfg)
