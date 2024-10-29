from moduslam.frontend_manager.graph.custom_vertices import Pose
from phd.bridge.edges_builder.edge_factories.protocol import EdgeFactory
from phd.external.objects.measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.element import GraphElement
from phd.moduslam.frontend_manager.main_graph.graph import Graph


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(cls, measurement: Measurement, graph: Graph) -> list[GraphElement]:
        """
        1)  pose = graph.find_closest_vertex(Pose) - O(log(N)) or O(1)

        2)  if pose:
                value = pose.value
            else:
                value = 0

            p = Pose(measurement.timestamp, value)

        3)  edge = GpsPosition(p, measurement.value, measurement.covariance)
            vertices_db.append(p)
            return [edge], [p]
        """
        raise NotImplementedError
