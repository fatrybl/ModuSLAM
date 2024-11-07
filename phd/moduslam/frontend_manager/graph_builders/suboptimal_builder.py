from moduslam.data_manager.batch_factory.batch import DataBatch, Element
from phd.bridge.optimal_candidate_factory import Factory
from phd.measurements.measurement_storage import MeasurementStorage
from phd.measurements.processed_measurements import Measurement
from phd.moduslam.frontend_manager.handlers.handler_protocol import Handler
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.config import (
    ImuHandlerConfig as ImuHandlerConfig,
)
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.kaist_urban_handler import (
    KaistUrbanImuDataPreprocessor,
)
from phd.moduslam.frontend_manager.handlers.scan_matcher.config import (
    KissIcpScanMatcherConfig,
)
from phd.moduslam.frontend_manager.handlers.scan_matcher.matcher import ScanMatcher
from phd.moduslam.frontend_manager.handlers.vrs_gps.config import VrsGpsHandlerConfig
from phd.moduslam.frontend_manager.handlers.vrs_gps.handler import (
    KaistUrbanVrsGpsPreprocessor,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement
from phd.moduslam.frontend_manager.measurement_storage_analyzers.single_pose_odometry import (
    Analyzer,
)


class Builder:
    """Creates multiple edges combinations and chooses the best one."""

    def __init__(
        self,
        configs: tuple[
            ImuHandlerConfig,
            VrsGpsHandlerConfig,
            KissIcpScanMatcherConfig,
            KissIcpScanMatcherConfig,
        ],
    ):
        self._analyzer = Analyzer()
        self._candidate_factory = Factory()
        self._storage = MeasurementStorage()

        handler1 = KaistUrbanImuDataPreprocessor(configs[0])
        handler2 = KaistUrbanVrsGpsPreprocessor(configs[1])
        handler3 = ScanMatcher(configs[2])
        handler4 = ScanMatcher(configs[3])

        self._handlers: list[Handler] = [handler1, handler2, handler3, handler4]

    def create_elements(self, data_batch: DataBatch, graph: Graph) -> list[GraphElement]:
        """Creates graph candidate using the measurements from the data batch.

        Args:
            data_batch: a data batch with elements.

            graph: a main graph to create graph elements for.

        Returns:
            new graph elements.
        """

        while not data_batch.empty:
            element = data_batch.first
            data_batch.remove_first()
            new_measurement = self._process_element(element)

            self._storage.add(new_measurement) if new_measurement else None

            enough_measurements = self._analyzer.check_storage(self._storage)

            if enough_measurements:
                candidate = self._candidate_factory.create_best_candidate(graph, self._storage)

                self._storage.clear()
                self._storage.add(candidate.leftovers)

                return candidate.elements

        return []

    def _process_element(self, element: Element) -> Measurement | None:
        """Processes an element with the appropriate handler.

        Args:
            element: element to be distributed and processed.

        Returns:
            new measurement or None.
        """
        sensor = element.measurement.sensor

        for handler in self._handlers:
            if handler.sensor_type == type(sensor) and handler.sensor_name == sensor.name:
                new_measurement = handler.process(element)

                if new_measurement:
                    return new_measurement

        return None
