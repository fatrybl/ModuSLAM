import logging
from collections.abc import Collection

import gtsam

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.custom_edges import PriorPose
from slam.frontend_manager.graph.custom_vertices import Pose
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.noise_models import pose_diagonal_noise_model
from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.auxiliary_methods import tuple_to_gtsam_pose3
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class PriorPoseEdgeFactory(EdgeFactory):
    def __init__(self, config: EdgeFactoryConfig):
        super().__init__(config)

    @staticmethod
    def noise_model(
        values: Collection[float],
    ) -> gtsam.noiseModel.Diagonal.Sigmas:
        """Diagonal Gaussian noise model for pose: [x, y, z, roll, pitch, yaw].

        Args:
            values (Collection[float]): measurement noise sigmas: [x, y, z, roll, pitch, yaw].

        Returns:
            noise model (gtsam.noiseModel.Diagonal.Sigmas).
        """
        return pose_diagonal_noise_model(values)

    @property
    def vertices_types(self) -> set[type[Pose]]:
        return {Pose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        return {gtsam.Pose3}

    def create(
        self, graph: Graph, vertices: Collection[Pose], measurements: OrderedSet[Measurement]
    ) -> list[PriorPose]:
        measurement: Measurement = measurements.last
        vertex = tuple(vertices)[0]
        edge = self._create_edge(vertex, measurement)
        return [edge]

    def _create_edge(self, vertex: Pose, measurement: Measurement) -> PriorPose:
        noise = self.noise_model(measurement.noise_covariance)

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
