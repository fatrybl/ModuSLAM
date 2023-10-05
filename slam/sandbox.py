from typing import Iterable
from collections.abc import Iterator

from plum import dispatch
from slam.setup_manager.sensor_factory.sensors import Sensor, Imu, Fog, Encoder
from pathlib import Path
from slam.test import TestClass


if __name__ == '__main__':
    imu = Imu('my_imu', Path(
        '/home/oem/Desktop/PhD/mySLAM/configs/sensors/imu.yaml'))
    test = TestClass()
    test.method(imu, 123)
    test.method(imu, '+++')
