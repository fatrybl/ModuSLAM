

import hydra
from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module
from dataclasses import dataclass, field
from email.policy import default
from pathlib import Path

from omegaconf import DictConfig

# from configs.sensors.base_sensor_parameters import Parameter
from configs.sensors.imu import ImuParameter
from configs.system.setup_manager.sensor_factory import Sensor

from slam.data_manager.factory.readers.element_factory import Element, Location, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import CsvDataLocation
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import VrsGps

from tests.data_manager.factory.readers.kaist.api.full_dataset.config import imu


@dataclass(frozen=True)
class TestLocation(Location):
    position: int
    file: str = 'test.file'


@dataclass
class Parameter:
    pose: dict[str, float] = field(default_factory=lambda: {'pose': 1.0})


cs = ConfigStore()
cs.store(name='cfg', node=Parameter)


# @hydra.main(config_name='cfg')
def run(cfg: DictConfig):

    print(cfg)

    el = Element(
        timestamp=1,
        measurement=Measurement(
            sensor=VrsGps('vrs', cfg),
            values=(1, 2, 3)),
        location=CsvDataLocation(file=Path(), position=0)
    )

    print(hash(cfg))


if __name__ == '__main__':
    run(DictConfig({"pose": (1, 2, 3)}))
