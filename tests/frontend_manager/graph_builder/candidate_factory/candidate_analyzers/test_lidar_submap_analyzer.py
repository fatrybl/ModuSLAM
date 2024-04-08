from unittest.mock import MagicMock

import pytest

from slam.frontend_manager.graph_builder.candidate_factory.candidate_analyzers.lidar_submap_analyzer import (
    LidarSubmapAnalyzer,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)


@pytest.fixture
def analyzer():
    return LidarSubmapAnalyzer()


def test_check_readiness_with_less_states(analyzer):
    mock_graph_candidate = MagicMock(spec=GraphCandidate)
    mock_graph_candidate.states = [1]  # Only one state
    assert analyzer.check_readiness(mock_graph_candidate)


def test_check_readiness_with_required_states(analyzer):
    mock_graph_candidate = MagicMock(spec=GraphCandidate)
    mock_graph_candidate.states = [1, 2]  # Two states
    assert not analyzer.check_readiness(mock_graph_candidate)


def test_check_readiness_with_more_states(analyzer):
    mock_graph_candidate = MagicMock(spec=GraphCandidate)
    mock_graph_candidate.states = [1, 2, 3]  # Three states
    assert not analyzer.check_readiness(mock_graph_candidate)
