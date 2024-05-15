from collections.abc import Collection

import gtsam

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.custom_vertices import LidarPose, Pose
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.frontend_manager.measurement_storage import Measurement
from slam.frontend_manager.noise_models import pose_diagonal_noise_model
from slam.system_configs.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarOdometryEdgeFactory(EdgeFactory):
    """Creates edges of type LidarOdometry."""

    def __init__(self, config: EdgeFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        super().__init__(config)
        self._time_margin: float = config.search_time_margin

    @property
    def vertices_types(self) -> set[type[LidarPose]]:
        """Types of the used vertices.

        Returns:
            set with 1 type (LidarPose).
        """
        return {LidarPose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        """Types of the used base (GTSAM) instances.

        Returns:
            set with 1 type (gtsam.Pose3).
        """
        return {gtsam.Pose3}

    def create(
        self, graph: Graph, vertices: Collection[LidarPose], measurements: OrderedSet[Measurement]
    ) -> list[LidarOdometry]:
        """Creates 1 edge (LidarOdometry) with the given measurements.

        Args:
            graph: the graph to create the edge for.

            vertices: graph vertices to be used for the new edge.

            measurements: contains SE(3) transformation matrix.

        Returns:
            list with 1 edge.
        """
        m: Measurement = measurements.last
        current_vertex = tuple(vertices)[0]
        index = current_vertex.index
        previous_vertex = self._get_previous_vertex(graph.vertex_storage, m.time_range.start, index)
        edge = self._create_edge(vertex1=previous_vertex, vertex2=current_vertex, measurement=m)
        return [edge]

    @staticmethod
    def _create_vertex(index: int, timestamp: int) -> LidarPose:
        """Creates the graph vertex.

        Args:
            index: index of the vertex.

            timestamp: timestamp of the vertex.

        Returns:
            new vertex.
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
        """Creates the GTSAM factor for the factor graph.

        Args:
            vertex1_id: id of the first vertex.

            vertex2_id: id of the second vertex.

            measurement: a measurement with values: transformation matrix SE(3).

            noise_model: GTSAM noise model.

        Returns:
            GTSAM factor.
        """
        tf = gtsam.Pose3(measurement.values)
        factor = gtsam.BetweenFactorPose3(
            key1=vertex1_id,
            key2=vertex2_id,
            relativePose=tf,
            noiseModel=noise_model,
        )
        return factor

    def _get_previous_vertex(self, storage: VertexStorage, timestamp: int, index: int) -> LidarPose:
        """Gets previous vertex if found or creates a new one.

        Args:
            storage: storage of vertices.

            timestamp: timestamp of the vertex.

            index: index of the vertex.

        Returns:
            vertex.
        """
        vertex = storage.get_last_vertex(LidarPose)
        if vertex:
            return vertex

        vertex = storage.find_closest_optimizable_vertex(Pose, timestamp, self._time_margin)
        if vertex:
            new_index = vertex.index
        else:
            new_index = index + 1

        new_vertex: LidarPose = self._create_vertex(index=new_index, timestamp=timestamp)
        return new_vertex

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

        factor = self._create_factor(vertex1.gtsam_index, vertex2.gtsam_index, measurement, noise)
        edge = LidarOdometry(
            vertex1=vertex1,
            vertex2=vertex2,
            factor=factor,
            measurements=(measurement,),
            noise_model=noise,
        )
        return edge
