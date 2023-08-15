import pytest
from yaml import dump
from enum import Enum
from pathlib import Path

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory

DEFAULT_CONFIG_PATH = Path(__file__).parent / "data_manager.yaml"


class ConfigEnum(Enum):
    config_path = DEFAULT_CONFIG_PATH


scenario1 = ({"data": {"dataset_type": "kaist",
                       "dataset_directory": "/home/oem/Downloads/urban18-highway/"}}, DataReader)

scenario2 = ({"data": {"dataset_type_S": "kaist_1",
                       "dataset_directory": "/home/oem/Downloads/urban18-highway/"}}, KeyError)

scenario3 = ({"data": {"dataset_type": "kaist_1",
                       "dataset_directory": "/home/oem/Downloads/urban18-highway/"}}, ValueError)

scenario4 = ({"data": {"dataset_type_S": "kaist",
                       "dataset_directory": "/home/oem/Downloads/urban18-highway/"}}, KeyError)

success_scenarios = [scenario1]
fail_scenarios = [scenario2, scenario3, scenario4]


def create_config_file(cfg: dict) -> None:
    with open(DEFAULT_CONFIG_PATH, 'w') as outfile:
        dump(cfg, outfile)


@pytest.mark.parametrize(
    ("test_cfg", "expected_output"), success_scenarios
)
def test_DataReaderFactory_success(test_cfg, expected_output):
    create_config_file(test_cfg)
    reader = DataReaderFactory(ConfigEnum.config_path.value)
    assert issubclass(type(reader), expected_output)


@pytest.mark.parametrize(
    ("test_cfg", "expected_output"), fail_scenarios
)
def test_DataReaderFactory_fail(test_cfg, expected_output):
    create_config_file(test_cfg)
    with pytest.raises(expected_output):
        reader = DataReaderFactory(ConfigEnum.config_path.value)
