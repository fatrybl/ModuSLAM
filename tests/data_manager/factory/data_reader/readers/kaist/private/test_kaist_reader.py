from pathlib import Path

import pytest

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import StreamConfig
from slam.utils.exceptions import FileNotValid
from tests_data.kaist_urban_dataset.data import DATASET_DIR


class TestKaistReader:
    """Tests for KaistReader constructor."""

    def test_kaist_reader_1(self):
        """Successful creation with proper configuration when the dataset exists and not
        empty."""
        dataset_cfg = KaistConfig(directory=DATASET_DIR)
        reader = KaistReader(dataset_cfg, StreamConfig())
        assert reader is not None

    def test_kaist_reader_2(self):
        """
        Unsuccessful creation with improper configuration: dataset path.
        """
        dataset_cfg = KaistConfig(directory=Path("some/invalid/dataset/path"))

        with pytest.raises(FileNotValid):
            KaistReader(dataset_cfg, StreamConfig())

    def test_kaist_reader_3(self):
        """
        Unsuccessful creation with improper configuration: data_stamp.csv file.
        """
        dataset_cfg = KaistConfig(directory=DATASET_DIR)
        dataset_cfg.data_stamp_file = Path("some/invalid/data_stamp.csv")

        with pytest.raises(FileNotValid):
            KaistReader(dataset_cfg, StreamConfig())
