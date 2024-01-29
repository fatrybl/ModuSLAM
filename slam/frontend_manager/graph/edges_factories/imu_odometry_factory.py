from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges.imu_odometry import ImuOdometry
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph


class ImuOdometryFactory(EdgeFactory):
    """
    Creates edges of type: ImuOdometry.
    """

    @classmethod
    def create(cls, graph: Graph, measurements: tuple[Measurement, ...]) -> tuple[ImuOdometry, ...]:
        """
        Adds the last measurement from IMU handler.
        The last measurement includes all integrated measurements.
        Args:
            graph:
            measurements:

        Returns:

        """
        edges: tuple[ImuOdometry, ...] = ()
        last_m = measurements[-1]
        new_edge = ImuOdometry(graph, last_m)
        edges += (new_edge,)
        return edges
