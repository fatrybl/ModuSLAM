from pathlib import Path

import numpy as np
import PIL.Image as Image

from src.moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from src.moduslam.data_manager.batch_factory.data_readers.locations import (
    CsvDataLocation,
    Location,
)
from src.moduslam.data_manager.batch_factory.utils import equal_elements
from src.moduslam.sensors_factory.configs import StereoCameraConfig
from src.moduslam.sensors_factory.sensors import Sensor, StereoCamera

_sensor = StereoCamera(StereoCameraConfig(name="test_camera"))


def test_equal_elements_identical():
    loc = Location()
    data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
    img = Image.fromarray(data)

    m = RawMeasurement(values=(img,), sensor=_sensor)

    element1 = Element(timestamp=123, location=loc, measurement=m)
    element2 = Element(timestamp=123, location=loc, measurement=m)

    assert equal_elements(element1, element2) is True


def test_equal_elements_none():
    assert equal_elements(None, None) is True


def test_equal_elements_one_none():
    loc = Location()
    data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
    img = Image.fromarray(data)

    m = RawMeasurement(values=(img,), sensor=_sensor)

    element = Element(timestamp=123, location=loc, measurement=m)

    assert equal_elements(element, None) is False
    assert equal_elements(None, element) is False


def test_equal_elements_different_locations():
    loc1 = Location()
    loc2 = CsvDataLocation(file=Path("random_file.csv"), position=0)
    data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
    img = Image.fromarray(data)

    m = RawMeasurement(values=(img,), sensor=_sensor)

    element1 = Element(timestamp=123, location=loc1, measurement=m)
    element2 = Element(timestamp=123, location=loc2, measurement=m)

    assert equal_elements(element1, element2) is False


def test_equal_elements_different_values():
    loc = Location()
    values1 = (1, 2, 3)
    values2 = (4, 5, 6)

    m1 = RawMeasurement(values=(values1,), sensor=_sensor)
    m2 = RawMeasurement(values=(values2,), sensor=_sensor)

    element1 = Element(timestamp=123, location=loc, measurement=m1)
    element2 = Element(timestamp=123, location=loc, measurement=m2)

    assert equal_elements(element1, element2) is False


def test_equal_elements_different_timestamps():
    loc = Location()
    data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
    img = Image.fromarray(data)

    m = RawMeasurement(values=(img,), sensor=_sensor)

    element1 = Element(timestamp=123, location=loc, measurement=m)
    element2 = Element(timestamp=456, location=loc, measurement=m)

    assert equal_elements(element1, element2) is False


def test_equal_elements_different_sensors():
    other_sensor = Sensor("other_sensor")
    loc = Location()
    data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
    img = Image.fromarray(data)

    m1 = RawMeasurement(values=(img,), sensor=_sensor)
    m2 = RawMeasurement(values=(img,), sensor=other_sensor)

    element1 = Element(timestamp=123, location=loc, measurement=m1)
    element2 = Element(timestamp=123, location=loc, measurement=m2)

    assert equal_elements(element1, element2) is False
