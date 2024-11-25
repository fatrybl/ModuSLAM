from phd.bridge.edge_factories.factory_protocol import EdgeFactory
from phd.bridge.edge_factories.utils import (
    create_vertex_i_with_status,
    find_cluster,
    get_new_items,
)
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    pose_block_diagonal_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity4x4


class Factory(EdgeFactory):

    @classmethod
    def create(
        cls, graph: Graph, clusters: dict[VertexCluster, TimeRange], measurement: PoseMeasurement
    ) -> GraphElement:
        """Creates a new edge with prior SE(3) pose factor.

        Args:
            graph: a main graph.

            clusters: clusters with time ranges.

            measurement: a measurement with pose SE(3).

        Returns:
            a new element.
        """
        t = measurement.timestamp
        position_cov = measurement.position_noise_covariance
        orientation_cov = measurement.orientation_noise_covariance
        storage = graph.vertex_storage

        cluster = find_cluster(storage, clusters, t)
        pose = create_vertex_i_with_status(Pose, storage, cluster, t, identity4x4)

        noise = pose_block_diagonal_noise_model(position_cov, orientation_cov)

        edge = PriorPose(pose.instance, measurement, noise)

        new_vertices = get_new_items([pose])

        return GraphElement(edge, new_vertices)
