from phd.measurements.measurement_storage import MeasurementStorage
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphCandidate


class Factory:
    @classmethod
    def create_candidates(cls, graph: Graph, storage: MeasurementStorage) -> list[GraphCandidate]:
        """Creates graph candidates.

        Args:
            graph: a main graph.

            storage: a storage with the measurements.
        """

        """
        1. Separate IMU measurements (if present) from others.
        2. Merge all other measurements into a common list.
        3. Check if any PoseOdometry measurements are present. If so, split those
            which start/stop are inside storage.time_range and replace then in the original list.
        4. Sort measurements.
        5. Combine measurements with equal timestamps to the MeasurementGroups
        6. Create all possible groups combinations: list[list[Cluster]] - N.
        7. Filter those combinations which have cycles determined by the SplitPoseOdometry measurements.

                    IF IMU measurements are present:
        8.1. for each clusters` combination (list[Cluster]) create all possible connections - M.
        8.2. for each clusters` combination and all connections combinations:
            - fill the connections with IMU measurements.
            - process leftovers.
        8.3. Process fake imu connections.
        8.4. create NxM ClusterWithLeftovers.

                    IF IMU measurements are not present:
        9. create and return N or NxM graph candidates.
        """

        raise NotImplementedError
