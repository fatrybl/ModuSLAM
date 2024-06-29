"""Tests for KaistReader constructor.

1) test_kaist_reader_1: Successful creation. 2) test_kaist_reader_2: Unsuccessful
creation with non-existent dataset directory. 3) test_kaist_reader_3: Unsuccessful
creation with non-existent data_stamp.csv file.
"""

from pathlib import Path

import pytest

from moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream
from tests.conftest import kaist_custom_dataset_dir


def test_kaist_reader_1():
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)
    reader = KaistReader(regime=Stream(), dataset_params=dataset_cfg)
    assert reader is not None


def test_kaist_reader_2():
    dataset_cfg = KaistConfig(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(NotADirectoryError):
        KaistReader(regime=Stream(), dataset_params=dataset_cfg)


def test_kaist_reader_3():
    dataset_cfg = KaistConfig(directory=kaist_custom_dataset_dir)
    dataset_cfg.data_stamp_file = Path("some/invalid/data_stamp.csv")

    with pytest.raises(FileNotFoundError):
        KaistReader(regime=Stream(), dataset_params=dataset_cfg)
