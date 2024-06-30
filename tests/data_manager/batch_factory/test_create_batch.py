"""Tests for BatchFactory.create_batch() overloaded methods.

All test cases must be run on any DataReader implementation.

1. create_batch ():
    1.1 all sensors, stream -> DataBatch
    1.2 all sensors, time limit includes all data -> DataBatch
    1.3 all sensors, time limit includes some data -> DataBatch
    1.4 some sensors, stream -> DataBatch
    1.5 some sensors, time limit includes all of them -> DataBatch
    1.6 some sensors, time limit includes some of them -> DataBatch
    1.7 some sensors, time limit includes none of them -> Empty DataBatch
    1.8 no sensors, stream -> Empty DataBatch
    1.9 no sensors, time limit includes all sensors -> Empty DataBatch
    1.10 Memory limit is too low: MemoryError

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

| Test case | KaistReader | Ros1Reader  | Ros2Reader  |
=======================================================
| 1.1       |      +      |      +      |             |
| 1.2       |      +      |      +      |             |
| 1.3       |      +      |      +      |             |
| 1.4       |      +      |      +      |             |
| 1.5       |      +      |      +      |             |
| 1.6       |      +      |      +      |             |
| 1.7       |      +      |      +      |             |
| 1.8       |      +      |      +      |             |
| 1.9       |      +      |      +      |             |
| 1.10      |      +      |      +      |             |
=======================================================
| 2.1       |      +      |      +      |             |
| 2.2       |      +      |      +      |             |
| 2.3       |      +      |      +      |             |
| 2.4       |      +      |      +      |             |
| 2.5       |      +      |      +      |             |
| 2.6       |      +      |      +      |             |
=======================================================
| 3.1       |      +      |      +      |             |
| 3.2       |      +      |      +      |             |
| 3.3       |      +      |      +      |             |
| 3.4       |      +      |      +      |             |
| 3.5       |      +      |      +      |             |
=======================================================
"""

from pytest import mark, raises

from moduslam.data_manager.batch_factory.batch import DataBatch, Element
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.system_configs.setup_manager.sensor_factory import SensorsFactoryConfig
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest
from moduslam.utils.auxiliary_methods import equal_batches
from moduslam.utils.exceptions import UnfeasibleRequestError
from tests.data_manager.batch_factory.test_cases.kaist.scenarios import (
    kaist_scenarios1_fail,
    kaist_scenarios2_fail,
    kaist_scenarios2_success,
    kaist_scenarios3_fail,
    kaist_scenarios3_success,
)
from tests.data_manager.batch_factory.test_cases.tum_vie.scenarios import (
    tum_vie_scenarios1_fail,
    tum_vie_scenarios1_success,
    tum_vie_scenarios2_fail,
    tum_vie_scenarios2_success,
    tum_vie_scenarios3_fail,
    tum_vie_scenarios3_success,
)

test_cases_1_success = (*tum_vie_scenarios1_success,)
test_cases_2_success = (*kaist_scenarios2_success, *tum_vie_scenarios2_success)
test_cases_3_success = (*kaist_scenarios3_success, *tum_vie_scenarios3_success)
test_cases_1_fail = (*kaist_scenarios1_fail, *tum_vie_scenarios1_fail)
test_cases_2_fail = (*kaist_scenarios2_fail, *tum_vie_scenarios2_fail)
test_cases_3_fail = (*kaist_scenarios3_fail, *tum_vie_scenarios3_fail)


@mark.parametrize("config1, config2, reference_batch", [*test_cases_1_success])
def test_create_batch_1_success(
    config1: SensorsFactoryConfig,
    config2: BatchFactoryConfig,
    reference_batch: DataBatch,
):
    SensorsFactory.init_sensors(config1)
    batch_factory = BatchFactory(config2)

    batch_factory.create_batch()
    result_batch = batch_factory.batch

    assert equal_batches(result_batch, reference_batch) is True


@mark.parametrize("config1, config2", [*test_cases_1_fail])
def test_create_batch_1_fail(
    config1: SensorsFactoryConfig,
    config2: BatchFactoryConfig,
):
    SensorsFactory.init_sensors(config1)
    batch_factory = BatchFactory(config2)

    with raises(MemoryError):
        batch_factory.create_batch()


@mark.parametrize("config1, config2, input_elements, reference_batch", [*test_cases_2_success])
def test_create_batch_2_success(
    config1: SensorsFactoryConfig,
    config2: BatchFactoryConfig,
    input_elements: list[Element],
    reference_batch: DataBatch,
):
    SensorsFactory.init_sensors(config1)
    batch_factory = BatchFactory(config2)

    batch_factory.create_batch(input_elements)
    result_batch = batch_factory.batch
    assert equal_batches(result_batch, reference_batch) is True


@mark.parametrize("config1, config2, input_elements", [*test_cases_2_fail])
def test_create_batch_2_fail(
    config1: SensorsFactoryConfig,
    config2: BatchFactoryConfig,
    input_elements: list[Element],
):
    SensorsFactory.init_sensors(config1)
    batch_factory = BatchFactory(config2)
    with raises(MemoryError):
        batch_factory.create_batch(input_elements)


@mark.parametrize(
    "config1, config2, periodic_data_request, reference_batch", [*test_cases_3_success]
)
def test_create_batch_3_success(
    config1: SensorsFactoryConfig,
    config2: BatchFactoryConfig,
    periodic_data_request: PeriodicDataRequest,
    reference_batch: DataBatch,
):

    SensorsFactory.init_sensors(config1)
    batch_factory = BatchFactory(config2)

    batch_factory.create_batch(periodic_data_request)
    result_batch = batch_factory.batch

    assert equal_batches(result_batch, reference_batch) is True


@mark.parametrize("config1, config2, data_request, reference_exception", [*test_cases_3_fail])
def test_create_batch_3_fail(
    config1: SensorsFactoryConfig,
    config2: BatchFactoryConfig,
    data_request: PeriodicDataRequest,
    reference_exception: type[MemoryError | UnfeasibleRequestError],
):
    SensorsFactory.init_sensors(config1)
    batch_factory = BatchFactory(config2)

    with raises(reference_exception):
        batch_factory.create_batch(data_request)
