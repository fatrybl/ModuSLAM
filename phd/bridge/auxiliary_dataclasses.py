from dataclasses import dataclass

from phd.measurement_storage.cluster import MeasurementCluster
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.main_graph.graph import GraphCandidate
from phd.utils.exceptions import ValidationError


@dataclass
class Connection:
    """A connection between 2 clusters with a continuous measurement."""

    cluster1: MeasurementCluster
    cluster2: MeasurementCluster

    def __post_init__(self):
        if self.cluster1 is self.cluster2:
            raise ValidationError("Connection can not be established between the same clusters.")


@dataclass
class ClustersWithConnections:
    """A combination of vertices & edges."""

    clusters: list[MeasurementCluster]
    connections: list[Connection]


@dataclass
class ClustersWithLeftovers:
    clusters: list[MeasurementCluster]
    leftovers: list[Measurement]


@dataclass
class CandidateWithClusters:
    """Graph candidate with clusters of measurements."""

    candidate: GraphCandidate
    clusters: list[MeasurementCluster]
