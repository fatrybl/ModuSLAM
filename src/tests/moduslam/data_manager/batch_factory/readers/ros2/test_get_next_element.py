"""Tests for overloads of get_next_element() method for Kaist Urban Dataset Reader.

1. get_next_element() -> Element | None:
    tests sequential reading of elements in different regimes.

2. get_next_element_of_sensor() -> Element | None:
    tests sequential reading of sensor`s elements in different regimes.
"""

from collections.abc import Iterable

from pytest import mark

from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2HumbleConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.ros2.reader import Ros2Reader
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.data_manager.batch_factory.utils import equal_elements
from src.moduslam.sensors_factory.configs import SensorConfig
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.tests.moduslam.data_manager.batch_factory.readers.ros2.S3E.data.case1 import (
    S3E_1,
)


@mark.parametrize(
    "sensors_configs, dataset_cfg, regime, reference_outputs",
    [*S3E_1],
)
def test_get_next_element(
    sensors_configs: Iterable[SensorConfig],
    dataset_cfg: Ros2HumbleConfig,
    regime: Stream | TimeLimit,
    reference_outputs: list[Element | None],
):
    SensorsFactory.init_sensors(sensors_configs)
    sensors = SensorsFactory.get_sensors()
    reader = Ros2Reader(dataset_cfg)
    reader.configure(regime, sensors)

    with reader:
        for reference in reference_outputs:
            result = reader.get_next_element()
            assert equal_elements(result, reference) is True


# @mark.parametrize(
#     "sensor_factory_cfg, dataset_cfg, regime, inputs, reference_outputs",
#     [*S3E_2],
# )
# def test_get_next_element_of_sensor(
#         sensor_factory_cfg: Iterable[SensorConfig],
#         dataset_cfg: Ros2HumbleConfig,
#         regime: Stream | TimeLimit,
#         inputs: list[Sensor],
#         reference_outputs: list[Element | None],
# ):
#     SensorsFactory.init_sensors(sensor_factory_cfg)
#     sensors = SensorsFactory.get_sensors()
#     reader = Ros2Reader(dataset_cfg)
#     reader.configure(regime, sensors)
#
#     with reader:
#         for sensor, reference in zip(inputs, reference_outputs):
#             result = reader.get_next_element(sensor)
#             assert equal_elements(result, reference) is True
