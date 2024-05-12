from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.measurement_storage import MeasurementStorage
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)


class LidarOdometryStateAnalyzer(StateAnalyzer):
    """Analyzer for lidar odometry measurements` handler.

    Adds new state if the storage contains a measurement with lidar pointcloud odometry.
    """

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)
        self._handler = HandlersFactory.get_handler(config.handlers_names[0])

    def evaluate(self, storage: MeasurementStorage) -> State | None:
        """Evaluates the storage and adds a new state if a lidar odometry measurement is
        present.

        Args:
            storage: a storage with measurements.

        Returns:
            new state or None.
        """
        lidar_odometry_measurements = storage.data[self._handler]
        if lidar_odometry_measurements:
            new_state = State()
            last_m = lidar_odometry_measurements[-1]
            new_state.add(last_m)
            return new_state
        else:
            return None


class LidarInertialOdometryStateAnalyzer(StateAnalyzer):

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)
        self._lidar_odometry_handler = HandlersFactory.get_handler(config.handlers_names[0])
        self._imu_odometry_handler = HandlersFactory.get_handler(config.handlers_names[1])

    def evaluate(self, storage: MeasurementStorage) -> State | None:
        """Evaluates the storage and adds a new state if a lidar odometry measurement is
        present. If IMU odometry is present, it is added to the state.

        Args:
            storage: a storage with measurements.

        Returns:
            new state or None.
        """

        try:
            lidar_odometry_measurements = storage.data[self._lidar_odometry_handler]
            imu_odometry_measurements = storage.data[self._imu_odometry_handler]
        except KeyError:
            return None

        if lidar_odometry_measurements:
            new_state = State()
            last_m = lidar_odometry_measurements[-1]
            new_state.add(last_m)

            if imu_odometry_measurements:
                new_state.add(imu_odometry_measurements)

            return new_state

        else:
            return None
