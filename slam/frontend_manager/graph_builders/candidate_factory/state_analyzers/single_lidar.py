import logging

from slam.frontend_manager.elements_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph.graph_candidate import State
from slam.frontend_manager.graph_builders.candidate_factory.state_analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.handlers.ABC_handler import ElementHandler
from slam.frontend_manager.handlers.pointcloud_matcher import PointcloudMatcher

logger = logging.getLogger(__name__)


class SingleLidarStateAnalyzer(StateAnalyzer):
    """
    Analyzer for lidar states.
    """

    def __init__(self) -> None:
        self._new_state_status: bool = False
        self._num_pointclouds: int = 1
        self._handler_type = PointcloudMatcher
        self._new_state: State | None = None

    @property
    def new_state(self):
        if self._new_state:
            return self._new_state
        else:
            raise ValueError

    @property
    def new_state_status(self) -> bool:
        """
        Indicates if enough measurements in storage to add a new state.
        Returns:
            (bool): new state readiness status.
        """
        return self._new_state_status

    @new_state_status.setter
    def new_state_status(self, status: bool) -> None:
        self._new_state_status = status

    def _get_handler(self, handler_type: type[ElementHandler], storage: MeasurementStorage) -> PointcloudMatcher | None:
        """
        Gets the handler of the given type.
        Args:
            handler_type (ElementHandler): type of the handler.
            storage (MeasurementStorage): storage with handlers and measurements.
        Returns:
            handler (type[ElementHandler]): handler of the given type.
        """
        for handler in storage.data.keys():
            if isinstance(handler, handler_type):
                return handler

    def evaluate(self, storage: MeasurementStorage) -> None:
        """
        Seeks for a measurement obtained with the point-cloud registration handler.
        If found, changes the new_state_status flag.
        Args:
            storage: a storage with the processed measurements from handlers
        """
        handler: PointcloudMatcher | None = self._get_handler(self._handler_type, storage)
        if not handler:
            msg = f"No handler with the type of: {self._handler_type} in Measurement Storage."
            logger.error(msg)
            raise ValueError(msg)

        measurements = storage.data[handler]
        num_measurements = len(measurements)
        if num_measurements == self._num_pointclouds:
            self._new_state_status = True
            state: State = State(storage)
