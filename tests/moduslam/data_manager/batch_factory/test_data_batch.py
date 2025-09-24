from unittest.mock import MagicMock

from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.data_manager.batch_factory.data_objects import Element, RawMeasurement
from moduslam.data_manager.batch_factory.data_readers.locations import Location


def test_is_sorted_empty_batch():
    """Test that an empty batch is considered sorted."""
    batch = DataBatch()
    assert batch.is_sorted is True


def test_is_sorted_single_element():
    """Test that a batch with a single element is considered sorted."""
    batch = DataBatch()
    m1 = MagicMock(spec=RawMeasurement)
    element = Element(timestamp=1, measurement=m1, location=Location())
    batch.add(element)
    assert batch.is_sorted is True


def test_is_sorted_sorted_batch():
    """Test that a batch with elements in sorted order is considered sorted."""
    batch = DataBatch()
    m1 = MagicMock(spec=RawMeasurement)
    m2 = MagicMock(spec=RawMeasurement)
    m3 = MagicMock(spec=RawMeasurement)
    elements = [
        Element(timestamp=1, measurement=m1, location=Location()),
        Element(timestamp=2, measurement=m2, location=Location()),
        Element(timestamp=3, measurement=m3, location=Location()),
    ]
    for element in elements:
        batch.add(element)
    assert batch.is_sorted is True


def test_is_sorted_unsorted_batch():
    """Test that a batch with elements out of order is not considered sorted."""
    batch = DataBatch()
    m1 = MagicMock(spec=RawMeasurement)
    m2 = MagicMock(spec=RawMeasurement)
    m3 = MagicMock(spec=RawMeasurement)
    elements = [
        Element(timestamp=2, measurement=m2, location=Location()),
        Element(timestamp=1, measurement=m1, location=Location()),
        Element(timestamp=3, measurement=m3, location=Location()),
    ]
    for element in elements:
        batch.add(element)
    assert batch.is_sorted is False


def test_is_sorted_equal_timestamps():
    """Test that a batch with elements having equal timestamps is considered sorted."""
    batch = DataBatch()
    m1 = MagicMock(spec=RawMeasurement)
    m2 = MagicMock(spec=RawMeasurement)
    elements = [
        Element(timestamp=1, measurement=m1, location=Location()),
        Element(timestamp=1, measurement=m2, location=Location()),
    ]
    for element in elements:
        batch.add(element)
    assert batch.is_sorted is True
