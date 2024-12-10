from dataclasses import dataclass

from phd.measurement_storage.cluster import Cluster
from phd.measurement_storage.measurements.base import Measurement


@dataclass
class Connection:
    """A connection between 2 clusters.

    Only for a continuous measurement.
    """

    cluster1: Cluster
    cluster2: Cluster


@dataclass
class ClustersWithConnections:
    """A combination of vertices & edges."""

    clusters: list[Cluster]
    connections: list[Connection]


@dataclass
class ClustersWithLeftovers:
    clusters: list[Cluster]
    leftovers: list[Measurement]
