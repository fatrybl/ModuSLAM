import gtsam

from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import LidarOdometry
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import LidarPose
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)
from slam.system_configs.system.frontend_manager.edge_factories.base_factory import (
    EdgeFactoryConfig,
)
from slam.utils.ordered_set import OrderedSet


class LidarOdometryEdgeFactory(EdgeFactory[LidarOdometry, LidarPose]):
    """Creates edges of type: LidarOdometry."""

    def __init__(self, config: EdgeFactoryConfig) -> None:
        self._name: str = config.name
        self._noise_model: gtsam.noiseModel = self._init_noise_model(config.noise_model)

    @staticmethod
    def _init_noise_model(cfg: str) -> gtsam.noiseModel.Diagonal:
        """
        Initializes the noise model.
        Args:
            cfg (str): configuration.

        Returns:
            (gtsam.noiseModel.Diagonal): noise model.

        TODO: add config parser and support of other noise models.
        """
        return gtsam.noiseModel.Diagonal.Sigmas([1, 1, 1])

    @property
    def name(self) -> str:
        """Name of the factory.

        Returns:
            (str): name of the factory.
        """
        return self._name

    @property
    def vertex_type(self) -> type[LidarPose]:
        """Type of the vertex used by the factory for edge creation.

        Returns:
            (type[LidarPose]): vertex type.
        """
        return LidarPose

    @property
    def base_vertex_type(self) -> type[gtsam.Pose3]:
        """Type of the base vertex used by the factory for edge creation.

        Returns:
            (type[gtsam.Pose3]): base vertex type.
        """
        return gtsam.Pose3

    def create(
        self, graph: Graph, vertex: LidarPose, measurements: OrderedSet[Measurement]
    ) -> list[LidarOdometry]:
        """
        Creates new edges from the given measurements.
        Args:
            graph (Graph): the graphs with factor.
            vertex (LidarPose): lidar pose vertex.
            measurements (OrderedSet[Measurement]): measurements from the corresponding handler.

        Returns:
            (list[LidarOdometry]): new lidar odometry edges.
        """
        v1: LidarPose = self._get_vertex(graph)
        v2: LidarPose = self._init_vertex(vertex)
        m: Measurement = measurements.last
        edge = self._create_edge(vertex1=v1, vertex2=v2, measurement=m)
        return [edge]

    @staticmethod
    def _get_vertex(graph: Graph) -> LidarPose:
        """Gets the vertex from the graph.

        Returns:
            (LidarPose): vertex from the graph.

        TODO: think about:
            vertices =_graph.vertex_storage.get_vertices(LidarPose)
        """
        v = graph.vertex_storage.lidar_pose.items[-1]
        return v

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
        noise_model: gtsam.noiseModel,
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
        tf = measurement.values
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
        factor = self._create_factor(vertex1.index, vertex2.index, measurement, self._noise_model)
        edge = LidarOdometry(
            elements=measurement.elements,
            vertices=(vertex1, vertex2),
            vertex1=vertex1.index,
            vertex2=vertex2.index,
            factor=factor,
            noise_model=self._noise_model,
        )
        return edge
