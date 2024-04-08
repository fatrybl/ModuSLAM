"""Tests for the LidarMapCandidateFactory class."""

from unittest.mock import patch

from slam.frontend_manager.element_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builder.candidate_factory.factories.lidar_submap import (
    LidarMapCandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.lidar_odometry import (
    LidarOdometryStateAnalyzer,
)
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from tests.frontend_manager.conftest import handler, measurement
from tests.frontend_manager.graph_builder.candidate_factory.conftest import (
    state_analyzer_config,
)


def test_lidar_map_candidate_factory_process_storage():
    factory = LidarMapCandidateFactory()
    storage = MeasurementStorage()
    factory.process_storage(storage)
    assert factory._previous_measurement is None


def test_lidar_map_candidate_factory_process_storage_with_measurement(
    measurement, handler, state_analyzer_config
):

    with patch.object(HandlersFactory, "get_handler", return_value=handler):

        factory = LidarMapCandidateFactory()
        factory._table = {handler: LidarOdometryStateAnalyzer(state_analyzer_config)}

        storage = MeasurementStorage()
        storage.add(measurement)

        factory.process_storage(storage)

        value = list(factory._graph_candidate.states[0].data.values())[0].first
        assert value == measurement
