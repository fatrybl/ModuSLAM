from moduslam.frontend_manager.graph.base_edges import Edge
from moduslam.frontend_manager.graph.base_vertices import Vertex
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from phd.bridge.edges_builder.edge_factories.protocol import EdgeFactory
from phd.bridge.objects.search_database import Database
from phd.external.objects.measurements import Odometry


class Factory(EdgeFactory):

    _vertex_type = LidarPose

    @classmethod
    def create(cls, measurement: Odometry, database: Database) -> tuple[list[Edge], list[Vertex]]:
        """Vertices = []

        1) cluster = graph.find_cluster(measurement.time_range.start) - O(log N)

            if cluster:
                lidar_pose = cluster.find_vertex(LidarPose) - O(1)
                if lidar_pose:
                    v1 = lidar_pose
                else:
                    any_pose = cluster.find_vertex(Pose) - O(log N)
                    if any_pose:
                        value = any_pose.value
                    else:
                        value = 0
                    v1 = LidarPose(measurement.time_range.start, value)
                    vertices.append(v1)

            else:
                v1 = LidarPose(measurement.time_range.start, 0)
                vertices.append(v1)

        2) v2 = LidarPose(measurement.time_range.stop, v1.value)
           vertices.append(v2)

        3) edge = LidarOdometryEdge(v1, v2, measurement.value, measurement.covariance)

        4) return [edge], vertices
        """
        raise NotImplementedError
