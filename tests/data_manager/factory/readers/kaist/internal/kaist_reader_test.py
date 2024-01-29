from pathlib import Path

from pytest import raises

from configs.system.data_manager.batch_factory.datasets.kaist import (
    KaistConfig,
    PairConfig,
)
from configs.system.data_manager.batch_factory.regime import RegimeConfig
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.utils.exceptions import FileNotValid
from tests.data_manager.factory.readers.kaist.conftest import Fixture


class TestKaistReader:
    """
    Tests for KaistReader constructor.
    """

    def test_kaist_reader(
        self,
        generate_dataset: Fixture,
        register_configs: Fixture,
        dataset_cfg: KaistConfig,
        regime_cfg: RegimeConfig,
    ):
        """
        Successfull KaistReader creation with proper configuration when the dataset exists and not empty.
        """

        reader = KaistReader(dataset_cfg, regime_cfg)
        assert reader is not None

    def test_kaist_reader_invalid_confgis_1(self, dataset_cfg: KaistConfig, regime_cfg: RegimeConfig):
        """
        Unsuccessfull KaistReader creation with improper configuration: dataset path.
        """

        dataset_cfg.directory = Path("some/invalid/dataset/path")

        with raises(FileNotValid):
            KaistReader(dataset_cfg, regime_cfg)

    def test_kaist_reader_invalid_confgis_2(self, dataset_cfg: KaistConfig, regime_cfg: RegimeConfig):
        """
        Unsuccessfull KaistReader creation with improper configuration: <SENSOR>.csv file.
        """

        dataset_cfg.iterable_data_files: list[PairConfig] = [
            PairConfig(sensor_name="some_sensor", location=Path("some/invalid/sensor_data.csv"))
        ]

        with raises(FileNotValid):
            KaistReader(dataset_cfg, regime_cfg)
