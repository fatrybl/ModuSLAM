"""
    TODO: add tests
"""

import gtsam

from moduslam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from moduslam.frontend_manager.edge_factories.utils import get_vertex
from moduslam.frontend_manager.graph.custom_edges import GpsPosition
from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.graph.graph import Graph
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
        super().__init__(config)
        self._time_margin = int(config.search_time_margin * self._second)

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
        vertex = get_vertex(Pose, graph.vertex_storage, timestamp, self._time_margin)
        edge = self._create_edge(vertex, measurements.last)
        return [edge]

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

        gtsam_factor = gtsam.GPSFactor(vertex.gtsam_index, measurement.values, noise)

        edge = GpsPosition(
            vertex=vertex, measurements=(measurement,), factor=gtsam_factor, noise_model=noise
        )
        return edge
