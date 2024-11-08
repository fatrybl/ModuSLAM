from phd.bridge.objects.auxiliary_classes import MeasurementGroup
from phd.bridge.objects.auxiliary_dataclasses import ClustersWithLeftovers
from phd.bridge.objects.measurements_cluster import Cluster
from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import Imu
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
        1. Separate IMU measurements (if present) from others. - [B]
        2. Merge all other measurements into a common list. - [B]
        3. Check if any PoseOdometry measurements are present. If so, split those
            which start/stop are inside storage.time_range and replace then in the original list. - [B]
        4. Sort measurements. - [B]
        5. Combine measurements with equal timestamps to the MeasurementGroups - [B]
        6. Create all possible groups combinations: list[list[Cluster]] - N. - [Ext]
        7. Filter those combinations which have cycles determined by the SplitPoseOdometry measurements. - [B]

                    IF IMU measurements are present:
        8.1. Create all possible clusters with connections: ClustersWithConnections - M. - [Ext]
        8.2. for each clusters` combination and all connections combinations: - [B]
            - fill the connections with IMU measurements:
            - process leftovers.
        8.3. Process fake imu connections. - [B]
        8.4. Create ClustersWithLeftovers. - [B]

                    IF IMU measurements are not present:
        9. create and return N or NxM graph candidates. - [B]
        """
        # =====================================
        """
        1. Prepare measurements: 1,2,3,4,5.
        2. Create combinations with External module.
        3. Filter out cycles.
        4. IF IMU: create and fill connections: 8.1-8.4
        5. Create ClustersWithLeftovers
        6. Create GraphCandidates.
        """

        raise NotImplementedError

    @staticmethod
    def _prepare_measurements(storage: MeasurementStorage) -> list[MeasurementGroup]:
        """Prepares measurements for further processing.

        Args:
            storage: a storage with the measurements.

        Returns:
            groups of measurements.
        """
        raise NotImplementedError

    @staticmethod
    def _create_combinations(measurement_groups: list[MeasurementGroup]) -> list[list[Cluster]]:
        """Creates all possible combinations of clusters.

        Args:
            measurement_groups: groups of measurements to combine.

        Returns:
            combinations of clusters.
        """
        raise NotImplementedError

    @staticmethod
    def _remove_cycles(combinations: list[list[Cluster]]) -> list[list[Cluster]]:
        """Removes combinations containing cycles.
        Cycle: a cluster with 2 SplitPoseOdometry measurements referencing the same PoseOdometry measurement.

        Args:
            combinations: combinations of clusters.

        Returns:
            combinations without cycles.
        """
        raise NotImplementedError

    @staticmethod
    def _process_continuous_measurements(
        combinations: list[list[Cluster]], measurements: list[Imu]
    ) -> list[ClustersWithLeftovers]:
        """Processes continuous measurements.

        Args:
            combinations: combinations of clusters.

            measurements: IMU measurements.

        Returns:
            clusters with unused measurements.
        """
        raise NotImplementedError
