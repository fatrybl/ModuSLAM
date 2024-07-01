"""Tests for DataReaderFactory.

For any Data Reader a valid dataset must be provided.

Test cases:
1) Both dataset and regime configs are valid -> DataReader
2) Dataset config is invalid: incorrect name of the data reader -> NotImplementedError
3) Regime config is invalid: incorrect name of the regime -> ValueError
"""

from pytest import mark, raises

from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.data_reader_factory import (
    DataReaderFactory,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import DataRegimeConfig
from tests.data_manager.batch_factory.data_reader_factory.scenarios import (
    invalid_dataset,
    invalid_regime,
    valid_readers,
)

valid_scenarios = (*valid_readers,)


@mark.parametrize(
    "dataset_config, regime_config, reference_reader",
    [*valid_scenarios],
)
def test_get_reader(
    dataset_config: DatasetConfig,
    regime_config: DataRegimeConfig,
    reference_reader: type[DataReader],
):
    reader = DataReaderFactory.create(dataset_config, regime_config)
    assert isinstance(reader, reference_reader)


@mark.parametrize(
    "dataset_config, regime_config",
    [invalid_dataset],
)
def test_get_reader_invalid_dataset(dataset_config: DatasetConfig, regime_config: DataRegimeConfig):
    with raises(NotImplementedError):
        DataReaderFactory.create(dataset_config, regime_config)


@mark.parametrize(
    "dataset_config, regime_config",
    [invalid_regime],
)
def test_get_reader_invalid_regime(dataset_config: DatasetConfig, regime_config: DataRegimeConfig):
    with raises(ValueError):
        DataReaderFactory.create(dataset_config, regime_config)
