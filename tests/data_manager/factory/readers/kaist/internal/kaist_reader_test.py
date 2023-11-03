from pathlib import Path
from typing import Type
from pytest import fixture, raises


from hydra.core.config_store import ConfigStore

from slam.utils.exceptions import FileNotValid
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

from configs.system.data_manager.batch_factory.regime import RegimeConfig, StreamConfig
from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig, PairConfig

from tests.data_manager.factory.readers.kaist.internal.config import KaistReaderConfig
from tests.data_manager.factory.readers.kaist.conftest import (
    DATASET_CONFIG_NAME, REGIME_CONFIG_NAME, Fixture)
from tests.data_manager.factory.readers.kaist.data_factory import DataFactory

from .data import (data_stamp,
                   stamp_files,
                   csv_data,
                   binary_data,
                   image_data)


@fixture(scope="class")
def create_dataset():
    data_factory = DataFactory()
    data_factory.create_dataset_structure()
    data_factory.generate_data(
        data_stamp,
        stamp_files,
        csv_data,
        binary_data,
        image_data)


@fixture(scope='class')
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=StreamConfig)


class TestKaistReader:
    """
    Tests for KaistReader constructor.
    """

    def test_kaist_reader(self, create_dataset: Fixture, register_configs: Fixture,
                          dataset_cfg: Type[KaistConfig], regime_cfg: Type[RegimeConfig]):
        """
        Successfull KaistReader creation with proper configuration when the dataset exists and not empty.
        """

        reader = KaistReader(dataset_cfg, regime_cfg)
        assert reader is not None

    def test_kaist_reader_invalid_confgis_1(self, dataset_cfg: Type[KaistConfig], regime_cfg: Type[RegimeConfig]):
        """
        Unsuccessfull KaistReader creation with improper configuration: dataset path.
        """

        dataset_cfg.directory = Path('some/invalid/dataset/path')

        with raises(FileNotValid):
            KaistReader(dataset_cfg, regime_cfg)

    def test_kaist_reader_invalid_confgis_2(self, dataset_cfg: Type[KaistConfig], regime_cfg: Type[RegimeConfig]):
        """
        Unsuccessfull KaistReader creation with improper configuration: <SENSOR>.csv file.
        """

        dataset_cfg.iterable_data_files: list[PairConfig] = [
            PairConfig(sensor_name='some_sensor',
                       location=Path('some/invalid/sensor_data.csv'))
        ]

        with raises(FileNotValid):
            KaistReader(dataset_cfg, regime_cfg)
