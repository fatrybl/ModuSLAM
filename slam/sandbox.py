

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
    print(hash(period1))
    print(hash(period2))
    print('--------------------------------')
    print(id(period1))
    print(id(period2))
    print(len(test_set))
