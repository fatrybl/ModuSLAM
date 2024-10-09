"""
    TODO: add tests
"""

import gtsam

from moduslam.frontend_manager.edge_factories.interface import EdgeFactory
from moduslam.frontend_manager.edge_factories.utils import get_last_vertex
from moduslam.frontend_manager.graph.base_vertices import OptimizableVertex
from moduslam.frontend_manager.graph.custom_edges import GpsPosition
from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.frontend_manager.noise_models import position_diagonal_noise_model
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.utils.ordered_set import OrderedSet


class GpsPositionEdgeFactory(EdgeFactory):
    """Creates edges of type GpsPosition."""

    _second: float = 1e9

    def __init__(self, config: EdgeFactoryConfig):
        """
        Args:
            config: configuration of the factory.
        """
        self._name: str = config.name
        self._time_margin = int(config.search_time_margin * self._second)

    @property
    def name(self) -> str:
        """Unique factory name."""
        return self._name

    def create(
        self, graph: Graph, measurements: OrderedSet[Measurement], timestamp: int
    ) -> list[GpsPosition]:
        """Creates 1 edge (GpsPosition) with the given measurement.

        Args:
            graph: the graph to create the edge for.

            measurements: contains SE(3) transformation matrix.

            timestamp: timestamp of the measurement.

        Returns:
            list with 1 edge.
        """
        vertex = self._get_vertex(graph.vertex_storage, timestamp, self._time_margin)
        if isinstance(vertex, Pose):
            edge = self._create_edge(vertex, measurements.last)
            return [edge]
        else:
            return []

    @staticmethod
    def _create_edge(vertex: Pose, measurement: Measurement) -> GpsPosition:
        """Creates the graph edge.

        Args:
            vertex: graph vertex to be used for the new edge.

            measurement: measurement with [x,y,z] position.

        Returns:
            new edge.
        """
        variances: tuple[float, float, float] = (
            measurement.noise_covariance[0],
            measurement.noise_covariance[1],
            measurement.noise_covariance[2],
        )
        noise: gtsam.noiseModel.Diagonal.Variances = position_diagonal_noise_model(variances)
        gtsam_factor = gtsam.GPSFactor(vertex.backend_index, measurement.value, noise)
        edge = GpsPosition(vertex, measurement, gtsam_factor, noise)
        return edge

    @staticmethod
    def _get_vertex(storage: VertexStorage, timestamp: int, time_margin: int) -> OptimizableVertex:
        """Gets the vertex to be used for the new edge.

        Args:
            storage: vertex storage.

            timestamp: timestamp of the new vertex.

            time_margin: time margin to search for the vertex.

        Returns:
            vertex to be used for the new edge.
        """
        vertex = get_last_vertex(Pose, storage, timestamp, time_margin)
        if vertex:
            return vertex

        opt_vertex = storage.find_closest_optimizable_vertex(Pose, timestamp, time_margin)
        if opt_vertex:
            return opt_vertex

        new_index = generate_index(storage.index_storage)
        vertex = Pose(timestamp=timestamp, index=new_index)
        return vertex
