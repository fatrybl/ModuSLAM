"""Distributes measurement to the corresponding edges factory."""

from phd.bridge.edges_builder.edge_factories.protocol import EdgeFactory
from phd.external.objects.measurements import Measurement

distribution_table: dict[object, object] = {}


def distribute(measurement: Measurement) -> EdgeFactory:
    """Distributes the measurement to the corresponding edges factory."""
    raise NotImplementedError
