import logging
from collections.abc import Collection

import gtsam

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.custom_edges import PriorPose
from slam.frontend_manager.graph.custom_vertices import Pose
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.noise_models import pose_diagonal_noise_model
from slam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.auxiliary_methods import tuple_to_gtsam_pose3
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class PriorPoseEdgeFactory(EdgeFactory):
    """Creates edges of type PriorPose."""

    def __init__(self, config: EdgeFactoryConfig):
        """
        Args:
            config: configuration of the factory.
        """
        super().__init__(config)

    @property
    def vertices_types(self) -> set[type[Pose]]:
        """Types of the used vertices.

        Returns:
            set with 1 type (Pose).
        """
        return {Pose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        """Types of the used base (GTSAM) instances.

        Returns:
            set with 1 type (gtsam.Pose3).
        """
        return {gtsam.Pose3}

    def create(
        self, graph: Graph, vertices: Collection[Pose], measurements: OrderedSet[Measurement]
    ) -> list[PriorPose]:
        """Creates 1 edge (PriorPose) with the given measurements.

        Args:
            graph: the graph to create the edge for.

            vertices: graph vertices to be used for the new edge.

            measurements: contains SE(3) transformation matrix.

        Returns:
            list with 1 edge.
        """
        measurement: Measurement = measurements.last
        vertex = tuple(vertices)[0]
        edge = self._create_edge(vertex, measurement)
        return [edge]

    @staticmethod
    def _create_edge(vertex: Pose, measurement: Measurement) -> PriorPose:
        """Creates the graph edge.

        Args:
            vertex: graph vertex to be used for the new edge.

            measurement: measurement with SE(3) transformation matrix.

        Returns:
            new edge.
        """
        variance: tuple[float, float, float, float, float, float] = (
            measurement.noise_covariance[0],
            measurement.noise_covariance[1],
            measurement.noise_covariance[2],
            measurement.noise_covariance[3],
            measurement.noise_covariance[4],
            measurement.noise_covariance[5],
        )
        noise: gtsam.noiseModel.Diagonal.Variances = pose_diagonal_noise_model(variance)

        pose = tuple_to_gtsam_pose3(measurement.values)

        gtsam_factor = gtsam.PriorFactorPose3(
            key=vertex.gtsam_index,
            prior=pose,
            noiseModel=noise,
        )

        edge = PriorPose(
            vertex=vertex, measurements=(measurement,), factor=gtsam_factor, noise_model=noise
        )
        return edge
