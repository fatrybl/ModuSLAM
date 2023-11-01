

import hydra
from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module
from dataclasses import dataclass, field
from email.policy import default
from pathlib import Path

from omegaconf import DictConfig

# from configs.sensors.base_sensor_parameters import Parameter
from configs.sensors.imu import ImuParameter
from configs.system.setup_manager.sensor_factory import SensorConfig

from slam.data_manager.factory.readers.element_factory import Element, Location, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import CsvDataLocation
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import VrsGps

from tests.data_manager.factory.readers.kaist.api.full_dataset.config import imu


@dataclass(frozen=True)
class tmp:
    position: int = 0
    file: str = 'test.file'


def run():
    t = tmp()
    print(t)


if __name__ == '__main__':
    run()
