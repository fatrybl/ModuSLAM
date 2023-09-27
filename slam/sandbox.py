from typing import Type
from dataclasses import dataclass
from typing import Iterable
from collections.abc import Iterator
from slam.setup_manager.sensor_factory.sensors import Imu, Fog, Encoder
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from pathlib import Path


def init_iterator(data: Iterable[float]) -> Iterator[float]:
    for element in data:
        yield element



if __name__ == '__main__':
    imu = Imu('imu', Path('/home/oem/Desktop/PhD/mySLAM/configs/sensors/imu.yaml'))
    fog = Fog('fog', Path('/home/oem/Desktop/PhD/mySLAM/configs/sensors/fog.yaml'))

    r1 = SensorData(imu, TimeLimit(0, 10))
    r2 = SensorData(fog, TimeLimit(0, 10))
    r3 = SensorData(imu, TimeLimit(20, 20))

    request = {r1, r2, r3}
    print(len(request))
