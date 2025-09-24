from dataclasses import dataclass

from moduslam.data_manager.batch_factory.config_factory import (
    get_config as get_bf_config,
)
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.external.metrics.orthogonality import PlaneOrthogonality
from moduslam.external.metrics.timeshift import TimeShift
from moduslam.external.metrics.vertices_connectivity import VerticesConnectivity
from moduslam.frontend_manager.main_graph.graph import GraphCandidate
from moduslam.map_manager.factories.lidar_map.config_factory import (
    get_config as get_pcd_config,
)
from moduslam.measurement_storage.cluster import MeasurementCluster


@dataclass
class MetricsResult:
    """Metrics result."""

    solver_error: float = 0.0
    connectivity: bool = False
    timeshift: int = 0
    num_unused_measurements: int = 0
    mom: float = 0.0


class MetricsFactory:
    """Manages all metrics."""

    def __init__(self):
        bf_config = get_bf_config()
        pcd_config = get_pcd_config()
        bf = BatchFactory(bf_config)
        self._mom = PlaneOrthogonality(pcd_config, bf)

    @staticmethod
    def compute_timeshift(clusters: list[MeasurementCluster]) -> int:
        """Computes timeshift metric.

        Args:
            clusters: clusters with measurements.

        Returns:
            timeshift metric.
        """
        value = TimeShift.compute(clusters)
        return value

    @staticmethod
    def compute_connectivity(candidate: GraphCandidate) -> bool:
        """Computes connectivity metric.

        Args:
            candidate: a graph candidate to evaluate connectivity for.

        Returns:
            connectivity metric.
        """
        all_vertices = candidate.graph.connections.keys()
        elements = candidate.elements
        value = VerticesConnectivity.compute(all_vertices, elements)
        return value

    def compute_mom(self, candidate: GraphCandidate) -> float:
        """Computes MOM metric.

        Args:
            candidate: a graph candidate to compute MOM metrics for.

        Returns:
            MOM metric.
        """
        connections = candidate.graph.connections
        elements = candidate.elements
        value = self._mom.compute(connections, elements)
        return value
