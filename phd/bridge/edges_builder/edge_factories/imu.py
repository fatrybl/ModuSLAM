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
        1) cluster = graph.find_closest_cluster(measurement.time_range.start) - O(log(N))

        2) if cluster:
                try to get pose, velocity, bias from the cluster.
                if all available:
                    use them as p_i, v_i, b_i
                else:
                    create new pose, velocity, bias. Maybe use some of them if already exist as init.
                    new_vertices.add(p_i)
                    new_vertices.add(v_i)
                    new_vertices.add(b_i)

            else:
                create new p_i, v_i, b_i with initial values = 0

        3)  create new p_j, v_j, b_j with initial values = 0
            new_vertices.add(p_j)
            new_vertices.add(v_j)
            new_vertices.add(b_j)

        4)  pim = gtsam.Preintegrate(measurement.values, start, stop, measurement.covariance)
            edge =  ImuOdometry(p_i, v_i, b_i, p_j, v_j, b_j, pim)

            return [edge], new_vertices
        """
        raise NotImplementedError
