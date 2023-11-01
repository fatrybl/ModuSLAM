from dataclasses import dataclass
from math import e
from pathlib import Path
from typing import Type

from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module
import pytest

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader


from configs.system.data_manager.regime import Stream
from slam.utils.exceptions import FileNotValid

from .config import (KaistReaderConfig,
                     DATASET_CONFIG_NAME, REGIME_CONFIG_NAME, CONFIG_MODULE_DIR)


class TestKaistReader:
    """
    Tests for KaistReader creation.
    """

    # def test_kaist_reader_valid_confgis(self, generate_data):
    #     """
    #     Successfull KaistReader creation with proper configuration when the dataset exists and not empty.

    #     Args:
    #         generate_data (_type_): fixture to generate Kaist Urban Dataset.
    #     """
    #     cs = ConfigStore.instance()
    #     cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    #     cs.store(name=REGIME_CONFIG_NAME, node=Stream)

    #     with initialize_config_module(config_module=CONFIG_MODULE_DIR):
    #         dataset_cfg = compose(config_name=DATASET_CONFIG_NAME)
    #         regime_cfg = compose(config_name=REGIME_CONFIG_NAME)
    #         KaistReader(dataset_cfg, regime_cfg)

    # def foo(self):
    #     with open('foo.txt') as f:
    #         for line in f:
    #             print("++++++++++++++++")
    #             yield line

    # def test_case(self):
    #     try:
    #         next(self.foo())
    #     except Exception as e:
    #         pytest.fail(str(e))

    def test_kaist_reader_invalid_confgis(self):
        """
        Successfull KaistReader creation with proper configuration when the dataset exists and not empty.

        Args:
            generate_data (_type_): fixture to generate Kaist Urban Dataset.
        """

        cs = ConfigStore.instance()
        cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
        cs.store(name=REGIME_CONFIG_NAME, node=Stream)

        with initialize_config_module(config_module=CONFIG_MODULE_DIR):
            dataset_cfg = compose(config_name=DATASET_CONFIG_NAME)
            regime_cfg = compose(config_name=REGIME_CONFIG_NAME)
            KaistReader(dataset_cfg, regime_cfg)