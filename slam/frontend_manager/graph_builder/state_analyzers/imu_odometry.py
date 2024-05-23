from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.graph_builder.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.frontend_manager.measurement_storage import Measurement
from slam.system_configs.frontend_manager.graph_builder.candidate_factory.state_analyzer import (
    StateAnalyzerConfig,
)
from slam.utils.auxiliary_methods import equal_numbers
from slam.utils.ordered_set import OrderedSet


class ImuOdometryAnalyzer(StateAnalyzer):
    """Analyzer for lidar odometry measurements` handler.

    Adds new state if the storage contains a measurement with lidar pointcloud odometry.
    """

    _nanoseconds_in_second: float = 1e9
    _tolerance: float = 0.01
    _integration_time: float = 1.05

    def __init__(self, config: StateAnalyzerConfig) -> None:
        """
        Args:
            config: configuration of the analyzer.
        """
        super().__init__(config)
        self._time_range = int(self._integration_time * self._nanoseconds_in_second)
        self._tolerance = int(self._tolerance * self._nanoseconds_in_second)
        self._state = State()
        self._update_state = False

    def evaluate(self, measurements: OrderedSet[Measurement]) -> State | None:
        """Evaluates a storage and creates a state if conditions are satisfied.

        Args:
            measurements: an ordered set of measurements.

        Returns:
            new state or None.
        """
        if self._update_state:
            self._clear()

        self._state.add(measurements.last)
        dt = self._state.time_range.stop - self._state.time_range.start
        print("dt=", dt * 1e-9)
        if equal_numbers(dt, self._time_range, self._tolerance):
            self._update_state = True
            print(f"adding new IMU state...: dt-range={abs(dt- self._time_range) * 1e-9}")
            return self._state

        return None

    def _clear(self) -> None:
        """Clears the analyzer state."""
        self._state = State()
        self._update_state = False
