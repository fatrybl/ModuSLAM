from dataclasses import dataclass

from moduslam.frontend_manager.main_graph.graph import GraphCandidate
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.imu import Imu
from moduslam.utils.exceptions import ValidationError


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
    """Measurements Clusters with leftovers and the number of unused measurements."""

    clusters: list[MeasurementCluster]
    leftovers: list[Imu]
    num_unused_measurements: int = 0

    def __post_init__(self):
        if self.num_unused_measurements < 0:
            raise ValidationError("Number of unused measurements can not be negative.")


@dataclass
class CandidateWithClusters:
    """Graph candidate with clusters of measurements."""

    candidate: GraphCandidate
    clusters: list[MeasurementCluster]
