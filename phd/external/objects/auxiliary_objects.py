from dataclasses import dataclass

from phd.external.objects.cluster import MeasurementsCluster
from phd.external.objects.measurements import CoreMeasurement


@dataclass
class Connection:
    """A connection between 2 clusters.

    Only for a continuous measurement.
    """

    cluster1: MeasurementsCluster
    cluster2: MeasurementsCluster


@dataclass
class ClustersWithConnections:
    """A combination of vertices & edges."""

    clusters: list[MeasurementsCluster]
    connections: list[Connection]


@dataclass
class ClustersWithLeftovers:
    clusters: list[MeasurementsCluster]
    leftovers: list[CoreMeasurement]
