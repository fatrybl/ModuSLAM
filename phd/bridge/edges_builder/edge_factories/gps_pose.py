from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from moduslam.frontend_manager.graph.custom_vertices import Pose
from phd.bridge.edges_builder.edge_factories.protocol import EdgeFactory
from phd.bridge.objects.search_database import Database
from phd.external.objects.measurements import Measurement


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(
        cls, measurement: Measurement, database: Database
    ) -> tuple[list[Edge], list[Vertex]]:
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
