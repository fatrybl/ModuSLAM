"""Tests for DataReaderFactory.

For any Data Reader a valid dataset must be provided.

Test cases:
1) Both dataset and regime configs are valid -> DataReader
2) Dataset config is invalid: incorrect name of the data reader -> NotImplementedError
3) Regime config is invalid: incorrect name of the regime -> ValueError
"""

from collections.abc import Iterable

from pytest import mark, raises

from src.moduslam.data_manager.batch_factory.configs import (
    DataRegimeConfig,
    DatasetConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.reader_ABC import DataReader
from src.moduslam.data_manager.batch_factory.data_readers.reader_factory import create
from src.moduslam.sensors_factory.configs import SensorConfig
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.tests.moduslam.data_manager.batch_factory.data_reader_factory.scenarios import (
    invalid_dataset,
    invalid_regime,
    valid_readers,
)

valid_scenarios = (*valid_readers,)


@mark.parametrize(
    "dataset_config, regime_config, sensors_configs, reference_reader",
    [*valid_scenarios],
)
def test_get_reader(
    dataset_config: DatasetConfig,
    regime_config: DataRegimeConfig,
    sensors_configs: Iterable[SensorConfig],
    reference_reader: type[DataReader],
):
    SensorsFactory.init_sensors(sensors_configs)

    reader, regime = create(dataset_config, regime_config)

    assert isinstance(reader, reference_reader)
    assert regime.name == regime_config.name


@mark.parametrize(
    "dataset_config, regime_config",
    [invalid_dataset],
)
def test_get_reader_invalid_dataset(dataset_config: DatasetConfig, regime_config: DataRegimeConfig):
    with raises(NotImplementedError):
        create(dataset_config, regime_config)


@mark.parametrize(
    "dataset_config, regime_config",
    [invalid_regime],
)
def test_get_reader_invalid_regime(dataset_config: DatasetConfig, regime_config: DataRegimeConfig):
    with raises(ValueError):
        create(dataset_config, regime_config)
