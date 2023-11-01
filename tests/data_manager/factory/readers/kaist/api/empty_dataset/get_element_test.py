from typing import Type
from omegaconf import DictConfig
from pytest import fixture, raises

from hydra.core.config_store import ConfigStore

from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensor_factory.sensors import Encoder
from slam.utils.exceptions import FileNotValid

from configs.system.data_manager.regime import Regime, Stream
from configs.system.data_manager.datasets.kaist import KaistConfig

from tests.data_manager.factory.readers.kaist.api.data_factory import DataFactory

from api.conftest import DATASET_CONFIG_NAME, REGIME_CONFIG_NAME
from .data import element
from .config import KaistReaderConfig


"""
Tests description:

1) Create a dataset for a DataReader.
2) Initialize config files for DataReader
3) Initialize DataReader with config files.
4) Test methods:
    4.1) get_element()
    4.2) get_element(element[Element])
    4.3) get_element(sensor[Sensor])
    4.4) get_element(sensor[Sensor], timestamp[int])
"""


@fixture(scope='class', autouse=True)
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=Stream)


@fixture(scope="class", autouse=True)
def generate_dataset():
    data_factory = DataFactory()
    data_factory.create_dataset_structure()


class TestGetElement:
    """
    All test should raise FileNotValidException as KaistReader object cannot be initialized properly 
    with empty '.csv' files. The Reader checks file validity before initializing files` iterators.
    """

    timestamp: int = 1
    sensor = Encoder('encoder', DictConfig({"params": ()}))
    element: Element = element

    def test_get_element_1(self, dataset_cfg: KaistConfig, regime_cfg: Type[Regime]):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            element: Element = reader.get_element()

    def test_get_element_2(self, dataset_cfg: KaistConfig, regime_cfg: Type[Regime]):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            element: Element = reader.get_element(self.element)

    def test_get_element_3(self, dataset_cfg: KaistConfig, regime_cfg: Type[Regime]):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            element: Element = reader.get_element(
                self.sensor)

    def test_get_element_4(self, dataset_cfg: KaistConfig, regime_cfg: Type[Regime]):
        with raises(FileNotValid):
            reader = KaistReader(dataset_cfg, regime_cfg)
            element: Element = reader.get_element(
                self.sensor, self.timestamp)
