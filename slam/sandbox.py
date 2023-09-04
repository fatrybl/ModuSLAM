
from plum import dispatch

from slam.data_manager.data_manager import DataManager


@dispatch
def get_imu():
    print('no args for imu')


@dispatch
def get_imu(*args):
    if args:
        pass
    else:
        print('')


def get_parser(sensor: str):
    if sensor == 'imu':
        return get_imu
    else:
        return None


if __name__ == '__main__':
    dm1 = DataManager()
    dm2 = DataManager()
    print(id(dm1) == id(dm2))
