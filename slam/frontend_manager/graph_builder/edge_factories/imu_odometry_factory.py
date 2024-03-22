import gtsam

from slam.frontend_manager.graph.edges import ImuOdometry
from slam.frontend_manager.graph.vertices import Pose
from slam.frontend_manager.graph_builder.edge_factories.edge_factory_ABC import (
    EdgeFactory,
)


class ImuOdometryFactory(EdgeFactory[ImuOdometry, Pose]):
    """
    Creates edges of type: ImuOdometry.
    """

    def __init__(self) -> None:
        self.noise_model: gtsam.noiseModel.Diagonal
        self.gtsam_factor: gtsam.ImuFactor

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def vertex_type(self) -> type[Pose]:
        return Pose

    @property
    def base_vertex_type(self) -> type[gtsam.Pose3]:
        return gtsam.Pose3

    def create_edge(self, values: tuple) -> None:
        """Creates an edge of type ImuOdometry.

        Args:
            values (tuple): values to create the edge.
        """
        pass
