from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange
from slam.utils.exceptions import ItemNotExistsError
from tests.data_manager.factory.batch_factory.test_data.readers.kaist.batches import (
    request1,
    request2,
)
from tests_data.kaist_urban_dataset.data import DATASET_DIR, el1, el25

cfg = KaistConfig(directory=DATASET_DIR)

sc1 = (
    (cfg, request1, el1),
    (cfg, request2, el25),
    (
        cfg,
        PeriodicData(sensor=el1.measurement.sensor, period=TimeRange(start=100500, stop=100500)),
        ItemNotExistsError(),
    ),
)
