"""
    TODO: add tests
"""

import gtsam

from moduslam.frontend_manager.edge_factories.interface import EdgeFactory
from moduslam.frontend_manager.edge_factories.utils import get_vertex
from moduslam.frontend_manager.graph.custom_edges import PriorPose
from moduslam.frontend_manager.graph.custom_vertices import Pose
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.frontend_manager.noise_models import pose_diagonal_noise_model
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.utils.auxiliary_methods import tuple_to_gtsam_pose3
from moduslam.utils.ordered_set import OrderedSet


class PriorPoseEdgeFactory(EdgeFactory):
    """Creates edges of type PriorPose."""

    def __init__(self, config: EdgeFactoryConfig):
        """
        Args:
            config: configuration of the factory.
        """
        self._name = config.name
        self._time_margin: int = 0

    @property
    def name(self) -> str:
        """Unique factory name."""
        return self._name

    def create(
        self, graph: Graph, measurements: OrderedSet[Measurement], timestamp: int
    ) -> list[PriorPose]:
        """Creates 1 edge (PriorPose) with the given measurements.

        Args:
            graph: the graph to create the edge for.

            measurements: contains SE(3) transformation matrix.

            timestamp: timestamp of prior measurement.

        Returns:
            list with 1 edge.
        """
        vertex = get_vertex(Pose, graph.vertex_storage, timestamp, self._time_margin)
        if isinstance(vertex, Pose):
            edge = self._create_edge(vertex, measurements.last)
            return [edge]
        else:
            return []

    @staticmethod
    def _create_edge(vertex: Pose, measurement: Measurement) -> PriorPose:
        """Creates the graph edge.

        Args:
            vertex: graph vertex to be used for the new edge.

            measurement: measurement with SE(3) transformation matrix.

        Returns:
            new edge.
        """
        variances: tuple[float, float, float, float, float, float] = (
            measurement.noise_covariance[0],
            measurement.noise_covariance[1],
            measurement.noise_covariance[2],
            measurement.noise_covariance[3],
            measurement.noise_covariance[4],
            measurement.noise_covariance[5],
        )
        noise: gtsam.noiseModel.Diagonal.Variances = pose_diagonal_noise_model(variances)

        pose = tuple_to_gtsam_pose3(measurement.value)

        gtsam_factor = gtsam.PriorFactorPose3(
            key=vertex.backend_index,
            prior=pose,
            noiseModel=noise,
        )

        edge = PriorPose(
            vertex=vertex, measurement=measurement, factor=gtsam_factor, noise_model=noise
        )
        return edge
