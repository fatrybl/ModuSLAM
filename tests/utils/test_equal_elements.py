from pathlib import Path

import numpy as np
import PIL.Image as Image

from slam.data_manager.factory.element import Element, Measurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import (
    CsvDataLocation,
    Location,
)
from slam.setup_manager.sensors_factory.sensors import Sensor, StereoCamera
from slam.system_configs.system.setup_manager.sensors_factory import SensorConfig
from slam.utils.auxiliary_methods import equal_elements


class TestEqualElements:

    sensor_config = SensorConfig(name="test_camera", type_name="StereoCamera")
    sensor = StereoCamera(sensor_config)

    other_sensor_config = SensorConfig(name="other_sensor", type_name="Sensor")
    other_sensor = Sensor(other_sensor_config)

    def test_equal_elements_identical(self):
        loc = Location()
        data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
        img = Image.fromarray(data)

        m = Measurement(values=(img,), sensor=self.sensor)

        element1 = Element(timestamp=123, location=loc, measurement=m)
        element2 = Element(timestamp=123, location=loc, measurement=m)

        assert equal_elements(element1, element2) is True

    def test_equal_elements_none(self):
        assert equal_elements(None, None) is True

    def test_equal_elements_one_none(self):
        loc = Location()
        data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
        img = Image.fromarray(data)

        m = Measurement(values=(img,), sensor=self.sensor)

        element = Element(timestamp=123, location=loc, measurement=m)

        assert equal_elements(element, None) is False
        assert equal_elements(None, element) is False

    def test_equal_elements_different_locations(self):
        loc1 = Location()
        loc2 = CsvDataLocation(file=Path("random_file.csv"), position=0)
        data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
        img = Image.fromarray(data)

        m = Measurement(values=(img,), sensor=self.sensor)

        element1 = Element(timestamp=123, location=loc1, measurement=m)
        element2 = Element(timestamp=123, location=loc2, measurement=m)

        assert equal_elements(element1, element2) is False

    def test_equal_elements_different_values(self):
        loc = Location()
        values1 = (1, 2, 3)
        values2 = (4, 5, 6)

        m1 = Measurement(values=(values1,), sensor=self.sensor)
        m2 = Measurement(values=(values2,), sensor=self.sensor)

        element1 = Element(timestamp=123, location=loc, measurement=m1)
        element2 = Element(timestamp=123, location=loc, measurement=m2)

        assert equal_elements(element1, element2) is False

    def test_equal_elements_different_timestamps(self):
        loc = Location()
        data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
        img = Image.fromarray(data)

        m = Measurement(values=(img,), sensor=self.sensor)

        element1 = Element(timestamp=123, location=loc, measurement=m)
        element2 = Element(timestamp=456, location=loc, measurement=m)

        assert equal_elements(element1, element2) is False

    def test_equal_elements_different_sensors(self):
        loc = Location()
        data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
        img = Image.fromarray(data)

        m1 = Measurement(values=(img,), sensor=self.sensor)
        m2 = Measurement(values=(img,), sensor=self.other_sensor)

        element1 = Element(timestamp=123, location=loc, measurement=m1)
        element2 = Element(timestamp=123, location=loc, measurement=m2)

        assert equal_elements(element1, element2) is False
