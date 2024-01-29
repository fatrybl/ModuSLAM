from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph


class SmartStereoLandmarkFactory(EdgeFactory):
    """
    Creates edges of type: SmartStereoLandmarkFactor.
    """

    @classmethod
    def create(cls, graph: Graph, measurements: tuple[Measurement, ...]) -> tuple[SmartStereoLandmark, ...]:
        edges: tuple[SmartStereoLandmark, ...] = ()
        for m in measurements:
            for landmark in m.values:
                new_edge = SmartStereoLandmark(landmark)
                edges += (new_edge,)

        return edges
