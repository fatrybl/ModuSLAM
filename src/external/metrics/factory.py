from dataclasses import dataclass

from src.bridge.auxiliary_dataclasses import CandidateWithClusters
from src.external.metrics.orthogonality import PlaneOrthogonality
from src.external.metrics.timeshift import TimeShift
from src.external.metrics.vertices_connectivity import VerticesConnectivity
from src.moduslam.backend_manager.graph_solver import GraphSolver
from src.moduslam.data_manager.batch_factory.config_factory import (
    get_config as get_bf_config,
)
from src.moduslam.data_manager.batch_factory.factory import BatchFactory
from src.moduslam.map_manager.map_factories.lidar_map.config_factory import (
    get_config as get_pcd_config,
)


@dataclass
class MetricsResult:
    """Metrics result."""

    mom: float
    solver_error: float
    connectivity: bool
    timeshift: int
    num_unused_measurements: int


class MetricsFactory:
    """Manages all metrics."""

    def __init__(self):
        bf_config = get_bf_config()
        pcd_config = get_pcd_config()
        bf = BatchFactory(bf_config)
        self._mom = PlaneOrthogonality(pcd_config, bf)
        self._solver = GraphSolver()

    def evaluate(self, item: CandidateWithClusters, error: float | None = None) -> MetricsResult:
        """Evaluates a candidate with measurement clusters.

        Args:
            item: a candidate with clusters of measurements to evaluate.

            error: solver error.

        Returns:
            metrics result.
        """
        graph = item.candidate.graph
        elements = item.candidate.elements
        connections = graph.connections
        all_vertices = connections.keys()
        num_unused = item.candidate.num_unused_measurements

        if error is None:
            _, error = self._solver.solve(graph)

        timeshift = TimeShift.compute(item.clusters)
        connectivity = VerticesConnectivity.compute(all_vertices, elements)
        mom = self._mom.compute(connections, elements)
        # mom = 0
        return MetricsResult(mom, error, connectivity, timeshift, num_unused)
