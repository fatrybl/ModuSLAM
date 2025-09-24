"""Tests for KaistReader instance."""

from pathlib import Path

import pytest

from moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from moduslam.data_manager.batch_factory.data_readers.kaist.reader import (
    KaistReader,
)
from moduslam.utils.exceptions import DataReaderConfigurationError, FileNotValid
from tests.conftest import kaist_custom_dataset_dir


def test_kaist_reader_successful_creation():
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)

    reader = KaistReader(dataset_params=dataset_cfg)

    assert reader is not None


def test_kaist_reader_invalid_dataset_directory():
    dataset_cfg = KaistConfig(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(DataReaderConfigurationError):
        KaistReader(dataset_params=dataset_cfg)


def test_kaist_reader_invalid_datastamp_file():
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)
    dataset_cfg.data_stamp_file = Path("some_invalid_data_stamp.csv")

    with pytest.raises(FileNotValid):
        KaistReader(dataset_params=dataset_cfg)
