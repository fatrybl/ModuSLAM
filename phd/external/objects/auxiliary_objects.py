from dataclasses import dataclass

from phd.external.objects.cluster import Cluster
from phd.external.objects.measurements import DiscreteMeasurement


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
    leftovers: list[DiscreteMeasurement]
