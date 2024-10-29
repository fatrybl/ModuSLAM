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
        new_vertices = []
        1)  pose = graph.find_closest_vertex(Pose) - O(log(N)) or O(1)

        2)  if pose:
                value = pose.value
            else:
                value = 0

            p = Pose(measurement.timestamp, value)
            new_vertices.append(p)

        3)  if multiple landmarks in the measurement:

                edges = []

                for landmark in measurement.landmarks:
                    1) is_present = graph.exists(landmark)
                    2) if is_present:
                            edge = PoseLandmark(p, landmark, landmark.value, landmark.covariance)
                            edges.append(edge)
                       else:
                            new_landmark = Landmark(timestamp, pose.value)
                            edge = PoseLandmark(p, new_landmark, landmark.value, landmark.covariance)
                            edges.append(edge)
                            new_vertices.append(new_landmark)

                return edges

            if single landmark in the measurement:

                is_present = graph.exists(measurement.landmark)

                if is_present:
                    edge = PoseLandmark(p, landmark, landmark.value, landmark.covariance)

                else:
                    new_landmark = Landmark(timestamp, pose.value)
                    edge = PoseLandmark(p, new_landmark, landmark.value, landmark.covariance)
                    new_vertices.append(new_landmark)

                 return [edge], new_vertices
        """
        raise NotImplementedError
