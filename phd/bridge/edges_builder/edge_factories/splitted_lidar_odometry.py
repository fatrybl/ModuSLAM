from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from phd.bridge.edges_builder.edge_factories.protocol import EdgeFactory
from phd.bridge.objects.search_database import Database
from phd.external.objects.measurements import SplittedOdometry


class Factory(EdgeFactory):

    _vertex_type = LidarPose

    @classmethod
    def create(
        cls, measurement: SplittedOdometry, database: Database
    ) -> tuple[list[Edge], list[Vertex]]:
        """Vertices = []

        1) parent = measurement.parent
           start = parent.time_range.start
           stop = parent.time_range.stop

        2)
            if measurement.timestamp == start:
                pose = graph.find_closest_vertex(Pose) - O(log(N))
                if pose:
                    value = pose.value
                else:
                    value = 0
                v1 = LidarPose(start, value)
                v2 = LidarPose(stop, value)

            else:
                # ignore this edge as it has already been added when measurement.timestamp == start
                return []

        3)
            edge = LidarOdometry(v1, v2, measurement.value, measurement.covariance)
            vertices_db.append(v1)
            vertices_db.append(v2)
            return [edge], vertices
        """
        raise NotImplementedError
