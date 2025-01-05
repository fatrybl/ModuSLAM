"""Tests for KaistReader constructor."""

from pathlib import Path

import pytest

from src.moduslam.data_manager.batch_factory.readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.configs import ImuConfig
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.tests.conftest import kaist_custom_dataset_dir
from src.utils.exceptions import DataReaderConfigurationError


def test_kaist_reader_successful_creation():
    SensorsFactory.init_sensors({"imu": ImuConfig("imu")})
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)

    reader = KaistReader(regime=Stream(), dataset_params=dataset_cfg)

    assert reader is not None


def test_kaist_reader_invalid_dataset_directory():
    dataset_cfg = KaistConfig(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(DataReaderConfigurationError):
        KaistReader(regime=Stream(), dataset_params=dataset_cfg)


def test_kaist_reader_invalid_datastamp_file():
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)
    dataset_cfg.data_stamp_file = Path("some_invalid_data_stamp.csv")

    with pytest.raises(DataReaderConfigurationError):
        KaistReader(regime=Stream(), dataset_params=dataset_cfg)


def test_kaist_reader_no_sensors():
    SensorsFactory.clear()
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)

    with pytest.raises(DataReaderConfigurationError):
        KaistReader(regime=Stream(), dataset_params=dataset_cfg)


def test_kaist_reader_sensors_regime_mismatch():
    SensorsFactory.clear()
    SensorsFactory.init_sensors({"imu": ImuConfig("imu")})
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)
    regime = TimeLimit(-1, 0)

    with pytest.raises(DataReaderConfigurationError):
        KaistReader(regime, dataset_cfg)
