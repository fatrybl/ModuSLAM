from phd.external.metrics.orthogonality import PlaneOrthogonality
from phd.external.metrics.storage import MetricsStorage
from phd.external.metrics.timeshift import TimeShift
from phd.external.metrics.vertices_connectivity import VerticesConnectivity
from phd.measurement_storage.cluster import MeasurementCluster
from phd.moduslam.backend_manager.graph_solver import GraphSolver
from phd.moduslam.frontend_manager.main_graph.graph import GraphCandidate


class MetricsFactory:
    """Manages all metrics."""

    def __init__(self):
        self._mom = PlaneOrthogonality()

    def evaluate(self, candidate: GraphCandidate, clusters: list[MeasurementCluster]) -> None:
        """Evaluates a candidate with measurement clusters.

        Args:
            candidate: a candidate to evaluate.

            clusters: measurement clusters for the candidate.
        """
        graph = candidate.graph
        connections = graph.connections
        all_vertices = connections.keys()

        solver = GraphSolver()
        values, error = solver.solve(graph)
        graph.update_vertices(values)

        timeshift = TimeShift.compute(clusters)
        connectivity = VerticesConnectivity.compute(all_vertices, candidate.elements)
        map_orthogonality = self._mom.compute(graph.vertex_storage, connections)

        MetricsStorage.add_mom(candidate, map_orthogonality)
        MetricsStorage.add_error(candidate, error)
        MetricsStorage.add_connectivity(candidate, connectivity)
        MetricsStorage.add_timeshift(candidate, timeshift)
