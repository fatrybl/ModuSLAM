"""1) test_kaist_reader_1:

Successful creation with proper configuration when the dataset exists and not empty. 2)
test_kaist_reader_2:     Unsuccessful creation with non-existent dataset directory. 3)
test_kaist_reader_3:     Unsuccessful creation with non-existent data_stamp.csv file.
"""

from pathlib import Path

import pytest

from moduslam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream
from moduslam.utils.exceptions import FileNotValid
from tests_data.kaist_urban_dataset.data import DATASET_DIR


class TestKaistReader:
    """Tests for KaistReader constructor."""

    def test_kaist_reader_1(self):
        dataset_cfg = KaistConfig(directory=DATASET_DIR)
        reader = KaistReader(regime=Stream(), dataset_params=dataset_cfg)
        assert reader is not None

    def test_kaist_reader_2(self):
        dataset_cfg = KaistConfig(directory=Path("some/invalid/dataset/path"))

        with pytest.raises(FileNotValid):
            KaistReader(regime=Stream(), dataset_params=dataset_cfg)

    def test_kaist_reader_3(self):
        dataset_cfg = KaistConfig(directory=DATASET_DIR)
        dataset_cfg.data_stamp_file = Path("some/invalid/data_stamp.csv")

        with pytest.raises(FileNotValid):
            KaistReader(regime=Stream(), dataset_params=dataset_cfg)
