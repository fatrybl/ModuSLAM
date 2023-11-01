from omegaconf import DictConfig
from pytest import fixture, raises
from unittest.mock import Mock, patch

from hydra.core.config_store import ConfigStore

from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

from configs.system.data_manager.regime import Stream
from slam.setup_manager.sensor_factory.sensors import Encoder
from slam.utils.exceptions import FileNotValid

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

    timestamp: int = 1
    sensor = Encoder('encoder', DictConfig({"params": ()}))
    element: Element = element

    def test_get_element_1(self, data_reader: KaistReader):
        with raises(FileNotValid):
            element: Element = data_reader.get_element()

    def test_get_element_2(self, data_reader: KaistReader):
        with raises(FileNotValid):
            element: Element = data_reader.get_element(self.element)

    def test_get_element_3(self, data_reader: KaistReader):
        with raises(FileNotValid):
            element: Element = data_reader.get_element(
                self.sensor)

#     def test_get_element_4(self, data_reader: KaistReader):
#         with raises(FileNotValid):
#             element: Element = data_reader.get_element(
#                 self.sensor, self.timestamp)
