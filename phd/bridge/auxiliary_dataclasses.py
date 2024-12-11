from dataclasses import dataclass

from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.base import Measurement


@dataclass
class Connection:
    """A connection between 2 clusters.

    Only for a continuous measurement.
    """

    cluster1: MeasurementCluster
    cluster2: MeasurementCluster


@dataclass
class ClustersWithConnections:
    """A combination of vertices & edges."""

    clusters: list[MeasurementCluster]
    connections: list[Connection]


@dataclass
class ClustersWithLeftovers:
    clusters: list[MeasurementCluster]
    leftovers: list[Measurement]
