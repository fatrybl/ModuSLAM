"""Tests for the ElementDistributor class."""

from unittest.mock import patch

import pytest

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.element import Element
from slam.frontend_manager.element_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.setup_manager.sensors_factory import SensorConfig
from slam.utils.ordered_set import OrderedSet
from tests.frontend_manager.element_distributor.conftest import create_measurement


@pytest.fixture
def sensor():
    cfg = SensorConfig(name="test_sensor", type_name="Sensor")
    return Sensor(config=cfg)


@pytest.fixture
def data_batch(element: Element) -> DataBatch:
    db = DataBatch()
    db.add(element)
    return db


def test_distribute_next(data_batch, sensor, handler):
    table = {sensor: [handler]}
    measurement = create_measurement(handler, data_batch.first)
    element_distributor = ElementDistributor()

    with patch.object(ElementDistributor, "sensor_handler_table", table):

        element_distributor.distribute_next(data_batch)
        assert measurement in element_distributor.storage.data[handler]


def test_clear_storage(handler, element):
    element_distributor = ElementDistributor()
    measurement = create_measurement(handler, element)
    element_distributor.storage.add(measurement)

    assert measurement in element_distributor.storage.data[handler]

    element_distributor.clear_storage([OrderedSet([measurement])])

    assert element_distributor.storage.is_empty
