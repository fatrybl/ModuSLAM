from collections import deque

import gtsam

from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import ImuOdometry
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex


class ImuOdometryFactory(EdgeFactory):
    """
    Creates edges of type: ImuOdometry.
    """

    def __init__(self) -> None:
        self.noise_model: gtsam.noiseModel.Diagonal
        self.gtsam_factor: gtsam.ImuFactor

    def create_edge(self, measurement: Measurement):
        """
        Creates new edge from the given measurement.
        Args:
            measurement:

        Returns:
            (ImuOdometry): new edge for Pre-integrated IMU measurements.

        TODO: think about parameters: id, vertices, gtsam_factor, noise_model...
        """
        # return ImuOdometry(id=new_id,
        #                    v1=,
        #                    v2=,
        #                    gtsam_factor=factor,
        #                    noise_model=self.noise_model,
        #                    vertices=,
        #                    elements=elements)

    @classmethod
    def create(cls, graph: Graph, vertices: set[Vertex], measurements: deque[Measurement]) -> list[ImuOdometry]:
        """
        Adds the last measurement from IMU handler.
        The last measurement includes all pre-integrated measurements.
        Args:
            graph (Graph): the main graph.
            vertices (set[Vertex]): vertices of the current state.
            measurements (deque[Measurement]): measurements from the handler.

        Returns:

        """
        ...
        edges: list[ImuOdometry] = []
        # m: Measurement = measurements[-1]
        # edge = cls.create_edge(m)
        # edges.append(edge)
        # return edges
        return edges
