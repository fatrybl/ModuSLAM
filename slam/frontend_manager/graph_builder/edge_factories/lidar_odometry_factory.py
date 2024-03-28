from collections.abc import Iterable

import gtsam

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.frontend_manager.graph.vertices import LidarPose
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)
from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarOdometryEdgeFactory(EdgeFactory):
    """Creates edges of type: LidarOdometry."""

    def __init__(self, config: EdgeFactoryConfig) -> None:
        self._time_margin: int = config.search_time_margin
        self._name: str = config.name
        self._noise_model: gtsam.noiseModel.Diagonal.Sigmas = self._init_noise_model(
            config.noise_model
        )

    @staticmethod
    def _init_noise_model(cfg: str) -> gtsam.noiseModel.Diagonal.Sigmas:
        """
        Initializes the noise model.
        Args:
            cfg (str): configuration.

        Returns:
            (gtsam.noiseModel.Diagonal): noise model.

        TODO: add config parser and support of other noise models.
        """
        return gtsam.noiseModel.Diagonal.Sigmas([1] * 6)

    @property
    def name(self) -> str:
        """Name of the factory.

        Returns:
            (str): name of the factory.
        """
        return self._name

    @property
    def vertices_types(self) -> set[type[LidarPose]]:
        """Type of the vertex used by the factory for edge creation.

        Returns:
            (type[LidarPose]): vertex type.
        """
        return {LidarPose}

    @property
    def base_vertices_types(self) -> set[type[gtsam.Pose3]]:
        """Type of the base vertex used by the factory for edge creation.

        Returns:
            (type[gtsam.Pose3]): base vertex type.
        """
        return {gtsam.Pose3}

    def create(
        self,
        graph: Graph,
        vertices: Iterable[LidarPose],
        measurements: OrderedSet[Measurement],
    ) -> list[LidarOdometry]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the graphs with factor.
            vertices (Iterable[LidarPose]): lidar pose vertex.
            measurements (OrderedSet[Measurement]): measurements from the corresponding handler.

        Returns:
            (list[LidarOdometry]): new lidar odometry edges.
        """
        m: Measurement = measurements.last
        current_vertex = list(vertices)[0]
        previous_vertex = self._find_vertex(graph.vertex_storage, m.time_range.start)
        if not previous_vertex:
            index = current_vertex.index - 1
            previous_vertex = self._create_vertex(index=index, timestamp=m.time_range.start)

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
            (LidarPose): new vertex.
        """
        vertex = LidarPose()
        vertex.index = index
        vertex.timestamp = timestamp
        return vertex

    def _find_vertex(self, storage: VertexStorage, timestamp: int) -> LidarPose | None:
        """Gets the vertex from the graph.

        Returns:
            (LidarPose): vertex from the graph.
        """

        v = storage.get_last_vertex(LidarPose)
        if v:
            return v

        v = storage.find_closest_vertex(LidarPose, timestamp, self._time_margin)
        if v:
            return v

        return None

    @staticmethod
    def _init_vertex(vertex: LidarPose) -> LidarPose:
        """Initializes attributes for the given vertex.

        Args:
            vertex (LidarPose): vertex to be initialized.

        Returns:
            (LidarPose): initialized vertex.
        """

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
            noise_model (gtsam.noiseModel): noise model.

        Returns:
            (gtsam.BetweenFactorPose3): lidar odometry factor.
        """
        tf = gtsam.Pose3(measurement.values)
        factor = gtsam.BetweenFactorPose3(
            key1=vertex1_id, key2=vertex2_id, relativePose=tf, noiseModel=noise_model
        )
        return factor

    def _create_edge(
        self, vertex1: LidarPose, vertex2: LidarPose, measurement: Measurement
    ) -> LidarOdometry:
        """Creates an edge instance.

        Returns:
            (LidarOdometry): edge instance.
        """

        factor = self._create_factor(
            vertex1.gtsam_index, vertex2.gtsam_index, measurement, self._noise_model
        )
        edge = LidarOdometry(
            vertex1=vertex1,
            vertex2=vertex2,
            factor=factor,
            measurements=(measurement,),
            noise_model=self._noise_model,
        )
        return edge
