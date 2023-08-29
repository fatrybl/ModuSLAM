
from plum import dispatch


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
    parser = get_parser(sensor='imu')
    parser()
