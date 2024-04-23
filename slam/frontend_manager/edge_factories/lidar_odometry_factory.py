from collections.abc import Collection

import gtsam

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.custom_vertices import LidarPose, Pose
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.frontend_manager.noise_models import pose_diagonal_noise_model
from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarOdometryEdgeFactory(EdgeFactory):
    """Creates edge of type: LidarOdometry."""

    def __init__(self, config: EdgeFactoryConfig) -> None:
        super().__init__(config)
        self._time_margin: int = config.search_time_margin

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
    def vertices_types(self) -> set[type[LidarPose]]:
        """Type of the vertex used by the factory for edge creation.

        Returns:
            vertex type (type[LidarPose]).
        """
        return {LidarPose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        """Type of the base vertex used by the factory for edge creation.

        Returns:
            base vertex type (type[gtsam.Pose3]).
        """
        return {gtsam.Pose3}

    def create(
        self, graph: Graph, vertices: Collection[LidarPose], measurements: OrderedSet[Measurement]
    ) -> list[LidarOdometry]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the graphs with factor.
            vertices (Collection[LidarPose]): lidar pose vertex.
            measurements (OrderedSet[Measurement]): measurements from the corresponding handler.

        Returns:
            new lidar odometry edges (list[LidarOdometry]).
        """
        m: Measurement = measurements.last
        current_vertex = tuple(vertices)[0]
        index = current_vertex.index
        previous_vertex = self._get_previous_vertex(graph.vertex_storage, m.time_range.start, index)
        edge = self._create_edge(vertex1=previous_vertex, vertex2=current_vertex, measurement=m)
        return [edge]

    @staticmethod
    def _create_vertex(index: int, timestamp: int) -> LidarPose:
        """
        Creates a new vertex.
        Args:
            index (int): index of the vertex.
            timestamp (int): timestamp of the vertex.

        Returns:
            new vertex (LidarPose).
        """
        vertex = LidarPose()
        vertex.index = index
        vertex.timestamp = timestamp
        return vertex

    @staticmethod
    def _create_factor(
        vertex1_id: int,
        vertex2_id: int,
        measurement: Measurement,
        noise_model: gtsam.noiseModel.Diagonal.Sigmas,
    ) -> gtsam.BetweenFactorPose3:
        """
        Creates a factor for the graph.
        Args:
            vertex1_id (int): id of the first vertex.
            vertex2_id (int): id of the second vertex.
            measurement (Measurement): transformation matrix SE(3).
            noise_model (gtsam.noiseModel.Diagonal.Sigmas): noise model.

        Returns:
            lidar odometry factor (gtsam.BetweenFactorPose3).
        """
        tf = gtsam.Pose3(measurement.values)
        factor = gtsam.BetweenFactorPose3(
            key1=vertex1_id, key2=vertex2_id, relativePose=tf, noiseModel=noise_model
        )
        return factor

    def _get_previous_vertex(self, storage: VertexStorage, timestamp: int, index: int) -> LidarPose:
        """Get previous vertex by finding or creating.

        Args:
            storage (VertexStorage): storage of vertices.
            timestamp (int): timestamp of the vertex.
            index (int): vertex index.

        Returns:
            (LidarPose): previous vertex.
        """
        vertex = storage.get_last_vertex(LidarPose)
        if vertex:
            return vertex

        vertex = storage.get_last_vertex(Pose)
        if vertex and vertex.timestamp == timestamp:
            new_index = vertex.index
        else:
            new_index = index + 1

        new_vertex: LidarPose = self._create_vertex(index=new_index, timestamp=timestamp)
        return new_vertex

    def _create_edge(
        self, vertex1: LidarPose, vertex2: LidarPose, measurement: Measurement
    ) -> LidarOdometry:
        """Creates an edge instance.

        Args:
            vertex1 (LidarPose): first vertex.
            vertex2 (LidarPose): second vertex.
            measurement (Measurement).

        Returns:
            edge instance (LidarOdometry).
        """
        noise = self.noise_model(measurement.noise_covariance)
        factor = self._create_factor(vertex1.gtsam_index, vertex2.gtsam_index, measurement, noise)
        edge = LidarOdometry(
            vertex1=vertex1,
            vertex2=vertex2,
            factor=factor,
            measurements=(measurement,),
            noise_model=noise,
        )
        return edge
