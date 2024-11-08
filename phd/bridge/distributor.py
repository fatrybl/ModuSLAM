"""Distributes measurement to the corresponding edges factory."""

from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.measurements.processed_measurements import Measurement

distribution_table: dict[object, object] = {}


def distribute(measurement: Measurement) -> EdgeFactory:
    """Distributes the measurement to the corresponding edges factory."""
    raise NotImplementedError
