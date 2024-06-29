"""Tests for TumVieReader constructor.

1) test_tum_vie_reader_1: Successful creation. 2) test_tum_vie_reader_2: Unsuccessful
creation with non-existent dataset directory. 3) test_tum_vie_reader_3: Unsuccessful
creation with non-existent data_stamp.csv file.
"""

from pathlib import Path

import pytest

from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream
from tests.conftest import tum_vie_dataset_dir


def test_tum_vie_reader_1():
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    reader = TumVieReader(regime=Stream(), dataset_params=dataset_cfg)
    assert reader is not None


def test_tum_vie_reader_2():
    dataset_cfg = TumVieConfig(directory=Path("some/invalid/dataset/path"))

    with pytest.raises(NotADirectoryError):
        TumVieReader(regime=Stream(), dataset_params=dataset_cfg)


def test_tum_vie_reader_3():
    dataset_cfg = TumVieConfig(directory=tum_vie_dataset_dir)
    dataset_cfg.csv_files = {dataset_cfg.imu_name: Path("some/invalid/data_stamp.csv")}

    with pytest.raises(FileNotFoundError):
        TumVieReader(regime=Stream(), dataset_params=dataset_cfg)
