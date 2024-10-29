from moduslam.frontend_manager.graph.custom_vertices import Pose
from phd.bridge.edges_builder.edge_factories.protocol import EdgeFactory
from phd.external.objects.measurements import Measurement
from phd.moduslam.frontend_manager.main_graph.element import GraphElement
from phd.moduslam.frontend_manager.main_graph.graph import Graph


class Factory(EdgeFactory):

    _vertex_type = Pose

    @classmethod
    def create(cls, measurement: Measurement, graph: Graph) -> list[GraphElement]:
        """Edges = [] vertices = []

        1)  pose = graph.find_closest_vertex(Pose) - O(log(N)) or O(1)

        2)  if pose:
                value = pose.value
            else:
                value = 0

            p = CameraPose(measurement.timestamp, value)
            vertices.append(p)

        3)  for landmark in measurement.landmarks:
                1) landmark = graph.get_landmark(landmark) - O(N).

                2) if landmark:
                        edge = graph.connections(landmark)
                        edge.add(p, measurement.value, measurement.covariance)
                   else:
                        new_landmark = Landmark(timestamp, pose.value)
                        edge = SmartFactor(camera_params)
                        edge.add(p, measurement.value, measurement.covariance)
                        TODO: add connection between new landmark and the edge
                                or let graph handles this automatically.
                        vertices.append(new_landmark)

                    edges.append(edge)

        4)  return edges, vertices
        """
        raise NotImplementedError
