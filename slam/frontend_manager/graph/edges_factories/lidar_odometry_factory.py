from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges.lidar_odometry import LidarOdometry
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph


class LidarOdometryFactory(EdgeFactory):
    """
    Creates edges of type: LidarOdometry.
    """

    @classmethod
    def create(cls, graph: Graph, measurements: tuple[Measurement, ...]) -> tuple[LidarOdometry, ...]:
        edges: tuple[LidarOdometry, ...] = ()
        for m in measurements:
            new_edge = LidarOdometry(graph, m)
            edges += (new_edge,)

        return edges
