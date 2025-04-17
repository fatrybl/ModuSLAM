"""Tests for BatchFactory class with different data readers and regimes.

1. create_batch ():
    1.1 all sensors, stream -> DataBatch
    1.2 all sensors, time limit includes all data -> DataBatch
    1.3 all sensors, time limit includes some data -> DataBatch
    1.4 some sensors, stream -> DataBatch
    1.5 some sensors, time limit includes all of them -> DataBatch
    1.6 some sensors, time limit includes some of them -> DataBatch
    1.7 some sensors, time limit includes none of them -> Empty DataBatch
    1.8 Memory limit is too low: MemoryError

2. create_batch (elements: Sequence[Element]):
    2.1 all element -> DataBatch
    2.2 one element -> DataBatch
    2.3 multiple valid elements -> DataBatch
    2.4 multiple equal elements -> DataBatch
    2.5 multiple elements: some equal, some different -> DataBatch
    2.6 Memory limit is too low: MemoryError

3. create_batch (request: PeriodicData):
    3.1 Regime and SensorsFactory configs are OK -> DataBatch
    3.2 Regime - OK, SensorsFactory: no sensors -> UnfeasibleRequestError
    3.3 Regime: invalid time margins, SensorsFactory - OK -> UnfeasibleRequestError
    3.4 Regime: invalid time margins, SensorsFactory: no sensors -> UnfeasibleRequestError
    3.5 Memory limit is too low: MemoryError


Checklist:

| Test case | Kaist Urban | Tum Vie | Ros2 (S3E) |
==================================================
| 1.1       |      +      |    +    |      +     |
| 1.2       |      +      |    +    |      +     |
| 1.3       |      +      |    +    |      +     |
| 1.4       |      +      |    +    |      +     |
| 1.5       |      +      |    +    |      +     |
| 1.6       |      +      |    +    |      +     |
| 1.7       |      +      |    +    |      +     |
| 1.8       |      +      |    +    |      +     |
==================================================
| 2.1       |      +      |    +    |      +     |
| 2.2       |      +      |    +    |      +     |
| 2.3       |      +      |    +    |      +     |
| 2.4       |      +      |    +    |      +     |
| 2.5       |      +      |    +    |      +     |
| 2.6       |      +      |    +    |      +     |
==================================================
| 3.1       |      +      |    +    |      +     |
| 3.2       |      +      |    +    |      +     |
| 3.3       |      +      |    +    |      +     |
| 3.4       |      +      |    +    |      +     |
| 3.5       |      +      |    +    |      +     |
==================================================
"""

from collections.abc import Iterable

from pytest import mark, raises

from src.moduslam.data_manager.batch_factory.batch import DataBatch, Element
from src.moduslam.data_manager.batch_factory.configs import BatchFactoryConfig
from src.moduslam.data_manager.batch_factory.factory import BatchFactory
from src.moduslam.data_manager.batch_factory.utils import equal_batches
from src.moduslam.sensors_factory.configs import SensorConfig
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.tests.moduslam.data_manager.batch_factory.test_cases.kaist.scenarios import (
    kaist_scenarios1_fail,
    kaist_scenarios1_success,
    kaist_scenarios2_fail,
    kaist_scenarios2_success,
    kaist_scenarios3_fail,
    kaist_scenarios3_success,
)
from src.tests.moduslam.data_manager.batch_factory.test_cases.ros2.scenarios import (
    ros2_s3e_scenarios1_fail,
    ros2_s3e_scenarios1_success,
    ros2_s3e_scenarios2_fail,
    ros2_s3e_scenarios2_success,
    ros2_s3e_scenarios3_fail,
    ros2_s3e_scenarios3_success,
)
from src.tests.moduslam.data_manager.batch_factory.test_cases.tum_vie.scenarios import (
    tum_vie_scenarios1_fail,
    tum_vie_scenarios1_success,
    tum_vie_scenarios2_fail,
    tum_vie_scenarios2_success,
    tum_vie_scenarios3_fail,
    tum_vie_scenarios3_success,
)
from src.utils.auxiliary_dataclasses import PeriodicDataRequest
from src.utils.exceptions import UnfeasibleRequestError

test_cases_1_success = (
    *kaist_scenarios1_success,
    *tum_vie_scenarios1_success,
    *ros2_s3e_scenarios1_success,
)
test_cases_2_success = (
    *kaist_scenarios2_success,
    *tum_vie_scenarios2_success,
    *ros2_s3e_scenarios2_success,
)
test_cases_3_success = (
    *kaist_scenarios3_success,
    *tum_vie_scenarios3_success,
    *ros2_s3e_scenarios3_success,
)
test_cases_1_fail = (
    kaist_scenarios1_fail,
    tum_vie_scenarios1_fail,
    ros2_s3e_scenarios1_fail,
)
test_cases_2_fail = (
    kaist_scenarios2_fail,
    tum_vie_scenarios2_fail,
    ros2_s3e_scenarios2_fail,
)
test_cases_3_fail = (
    *kaist_scenarios3_fail,
    *tum_vie_scenarios3_fail,
    *ros2_s3e_scenarios3_fail,
)


@mark.parametrize("sensors_configs, batch_factory_config, reference_batch", [*test_cases_1_success])
def test_create_batch_sequentially(
    sensors_configs: Iterable[SensorConfig],
    batch_factory_config: BatchFactoryConfig,
    reference_batch: DataBatch,
):
    SensorsFactory.init_sensors(sensors_configs)
    batch_factory = BatchFactory(batch_factory_config)

    batch_factory.fill_batch_sequentially()

    assert equal_batches(batch_factory.batch, reference_batch) is True


@mark.parametrize("sensors_configs, batch_factory_config", [*test_cases_1_fail])
def test_create_batch_sequentially_memory_error(
    sensors_configs: Iterable[SensorConfig], batch_factory_config: BatchFactoryConfig
):
    SensorsFactory.init_sensors(sensors_configs)
    batch_factory = BatchFactory(batch_factory_config)

    with raises(MemoryError):
        batch_factory.fill_batch_sequentially()


@mark.parametrize(
    "sensors_configs, batch_factory_config, input_elements, reference_batch",
    [*test_cases_2_success],
)
def test_create_batch_with_elements(
    sensors_configs: Iterable[SensorConfig],
    batch_factory_config: BatchFactoryConfig,
    input_elements: list[Element],
    reference_batch: DataBatch,
):
    SensorsFactory.init_sensors(sensors_configs)
    batch_factory = BatchFactory(batch_factory_config)

    batch_factory.fill_batch_with_elements(input_elements)

    assert equal_batches(batch_factory.batch, reference_batch) is True


@mark.parametrize("sensors_configs, batch_factory_config, input_elements", [*test_cases_2_fail])
def test_create_batch_with_elements_memory_error(
    sensors_configs: Iterable[SensorConfig],
    batch_factory_config: BatchFactoryConfig,
    input_elements: list[Element],
):
    SensorsFactory.init_sensors(sensors_configs)
    batch_factory = BatchFactory(batch_factory_config)
    with raises(MemoryError):
        batch_factory.fill_batch_with_elements(input_elements)


@mark.parametrize(
    "sensors_configs, batch_factory_config, periodic_data_request, reference_batch",
    [*test_cases_3_success],
)
def test_create_batch_by_request(
    sensors_configs: Iterable[SensorConfig],
    batch_factory_config: BatchFactoryConfig,
    periodic_data_request: PeriodicDataRequest,
    reference_batch: DataBatch,
):
    SensorsFactory.init_sensors(sensors_configs)
    batch_factory = BatchFactory(batch_factory_config)

    batch_factory.fill_batch_by_request(periodic_data_request)

    assert equal_batches(batch_factory.batch, reference_batch) is True


@mark.parametrize(
    "sensors_configs, batch_factory_config, data_request, reference_exception", [*test_cases_3_fail]
)
def test_create_batch_3_by_request_with_exception(
    sensors_configs: Iterable[SensorConfig],
    batch_factory_config: BatchFactoryConfig,
    data_request: PeriodicDataRequest,
    reference_exception: type[MemoryError | UnfeasibleRequestError],
):
    SensorsFactory.init_sensors(sensors_configs)
    batch_factory = BatchFactory(batch_factory_config)

    with raises(reference_exception):
        batch_factory.fill_batch_by_request(data_request)
