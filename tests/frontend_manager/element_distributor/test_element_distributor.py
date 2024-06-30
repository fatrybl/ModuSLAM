"""Tests for the ElementDistributor class."""

from unittest.mock import patch

import pytest

from moduslam.data_manager.batch_factory.batch import DataBatch, Element
from moduslam.frontend_manager.elements_distributor import ElementDistributor
from moduslam.utils.ordered_set import OrderedSet
from tests.frontend_manager.conftest import (  # noqa: F401, F811
    create_measurement,
    element,
    handler,
    sensor,
)


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

        element_distributor.distribute_element(data_batch.first)
        assert measurement in element_distributor.storage.data[handler]


def test_clear_storage(handler, element):
    element_distributor = ElementDistributor()
    z = create_measurement(handler, element)
    element_distributor.storage.add(z)

    assert z in element_distributor.storage.data[handler]

    element_distributor.clear_storage([OrderedSet([z])])

    assert element_distributor.storage.empty
