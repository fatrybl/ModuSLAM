"""
    TODO: add tests
"""

import gtsam

from moduslam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from moduslam.frontend_manager.edge_factories.utils import get_last_vertex
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose, Pose
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.graph.index_generator import generate_index
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.frontend_manager.noise_models import pose_diagonal_noise_model
from moduslam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from moduslam.utils.auxiliary_methods import sec2nanosec
from moduslam.utils.ordered_set import OrderedSet


class LidarOdometryEdgeFactory(EdgeFactory):
    """Creates edges of type LidarOdometry."""

    def __init__(self, config: EdgeFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        super().__init__(config)
        self._time_margin: int = sec2nanosec(config.search_time_margin)

    def create(
        self, graph: Graph, measurements: OrderedSet[Measurement], timestamp: int
    ) -> list[LidarOdometry]:
        """Creates 1 edge (LidarOdometry) with the given measurements.

        Args:
            graph: the graph to create the edge for.

            measurements: contains SE(3) transformation matrix.

            timestamp: timestamp of the j-th lidar pose.

        Returns:
            list with 1 edge.
        """
        m = measurements.last
        t_start = m.time_range.start
        t_stop = timestamp

        pose_i, pose_j = self._get_vertices(
            graph.vertex_storage, t_start, t_stop, self._time_margin
        )

        edge = self._create_edge(vertex1=pose_i, vertex2=pose_j, measurement=m)
        return [edge]

    @staticmethod
    def _create_factor(
        vertex1_id: int,
        vertex2_id: int,
        measurement: Measurement,
        noise_model: gtsam.noiseModel.Diagonal.Variances,
    ) -> gtsam.BetweenFactorPose3:
        """Creates the GTSAM factor for the factor graph.

        Args:
            vertex1_id: id of the first vertex.

            vertex2_id: id of the second vertex.

            measurement: a measurement with values: transformation matrix SE(3).

            noise_model: GTSAM noise model.

        Returns:
            GTSAM factor.
        """
        tf = gtsam.Pose3(measurement.value)
        factor = gtsam.BetweenFactorPose3(
            key1=vertex1_id,
            key2=vertex2_id,
            relativePose=tf,
            noiseModel=noise_model,
        )
        return factor

    def _create_edge(
        self, vertex1: LidarPose, vertex2: LidarPose, measurement: Measurement
    ) -> LidarOdometry:
        """Creates an edge.

        Args:
            vertex1: first vertex.

            vertex2: second vertex.

            measurement: a measurement with the transformation matrix SE(3).

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

        factor = self._create_factor(
            vertex1.backend_index, vertex2.backend_index, measurement, noise
        )
        edge = LidarOdometry(
            vertex1=vertex1,
            vertex2=vertex2,
            factor=factor,
            measurement=measurement,
            noise_model=noise,
        )
        return edge

    @staticmethod
    def _get_vertices(
        storage: VertexStorage,
        t1: int,
        t2: int,
        time_margin: int,
    ) -> tuple[LidarPose, LidarPose]:
        """Gets vertices with the given timestamps.

        Args:
            storage: storage of vertices.

            t1: timestamp of the 1-st vertex.

            t2: timestamp of the 2-nd vertex.

            time_margin: time margin for the search.

        Returns:
            2 vertices.
        """
        v1 = get_last_vertex(LidarPose, storage, t1, time_margin)
        if not v1:
            p = get_last_vertex(Pose, storage, t1, time_margin)
            if p:
                v1 = LidarPose(timestamp=p.timestamp, index=p.index, value=p.value)

        v2 = get_last_vertex(LidarPose, storage, t2, time_margin)
        if not v2:
            p = get_last_vertex(Pose, storage, t2, time_margin)
            if p:
                v2 = LidarPose(timestamp=p.timestamp, index=p.index, value=p.value)

        if v1 and v2:
            return v1, v2

        new_index = generate_index(storage.index_storage)

        if v1 and not v2:
            v2 = LidarPose(timestamp=t2, index=new_index, value=v1.value)
            return v1, v2

        elif v2 and not v1:
            v1 = LidarPose(timestamp=t1, index=new_index, value=v2.value)
            return v1, v2

        else:
            v1 = LidarPose(timestamp=t1, index=new_index)
            v2 = LidarPose(timestamp=t2, index=new_index + 1)
            return v1, v2
