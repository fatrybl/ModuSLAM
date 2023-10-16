

from dataclasses import dataclass

from slam.data_manager.factory.readers.element_factory import Element, Location, Measurement
from slam.setup_manager.sensor_factory.sensors import Sensor, Imu, Fog, Encoder
from pathlib import Path
from slam.utils.auxiliary_dataclasses import PeriodicData, TimeRange


if __name__ == '__main__':
    imu1 = Imu('imu1', Path(
        '/home/oem/Desktop/PhD/mySLAM/configs/sensors/imu.yaml'))
    imu2 = Imu('imu1', Path(
        '/home/oem/Desktop/PhD/mySLAM/configs/sensors/imu.yaml'))

    period1 = PeriodicData(imu1, TimeRange(0, 10))
    period2 = PeriodicData(imu2, TimeRange(0, 10))
    test_set = set({period1, period2})

    @dataclass(frozen=True)
    class TestLocation(Location):
        position: int
        file: str = 'test.file'

    m1 = Measurement(imu1, ('a', 'b', 'c'))
    l1 = TestLocation(0)
    e1 = Element(0, m1, l1)

    m2 = Measurement(imu1, ('a', 'b', 'c'))
    l2 = TestLocation(0)
    e2 = Element(0, m2, l2)

    m3 = Measurement(imu1, (1, 'b', True))
    l3 = TestLocation(2)
    e3 = Element(0, m3, l3)

    test_set = set((e1, e2, e3))
    # print(test_set)

    tup = (1, 2, 3)
    tup = (*tup, 4)

    print(tup)
