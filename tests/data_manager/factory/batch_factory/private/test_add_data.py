"""Test the _add_data(request: PeriodicData) method of the BatchFactory class.

Other overloads of _add_data() method are too naive to be tested.
"""

import pytest
from pytest import mark

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.element import Element
from slam.system_configs.system.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import StreamConfig
from slam.utils.auxiliary_dataclasses import PeriodicData
from slam.utils.auxiliary_methods import equal_elements
from tests.data_manager.factory.batch_factory.private.scenarios import sc1

test_cases = (*sc1,)


class TestAddData:

    @mark.parametrize("cfg, periodic_data, reference_result", [*test_cases])
    def test_add_data_1(
        self,
        cfg: DatasetConfig,
        periodic_data: PeriodicData,
        reference_result: Element | Exception,
    ):

        bf_cfg = BatchFactoryConfig(
            regime=StreamConfig(),
            memory=MemoryAnalyzerConfig(batch_memory=100),
            dataset=cfg,
        )

        batch_factory = BatchFactory(bf_cfg)

        if isinstance(reference_result, Exception):
            with pytest.raises(reference_result.__class__):
                batch_factory._add_data(periodic_data)
        else:
            batch_factory._add_data(periodic_data)
            element = batch_factory.batch.first_element
            equal_elements(element, reference_result)
