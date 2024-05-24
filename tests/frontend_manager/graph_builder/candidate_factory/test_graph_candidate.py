from collections import deque

import pytest

from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate_state import (
    State,
)
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.utils.auxiliary_dataclasses import TimeRange
from tests.frontend_manager.conftest import element, handler


@pytest.fixture
def measurements(handler, element):
    return [
        Measurement(
            time_range=TimeRange(1, 1),
            values=(1, 2, 3),
            handler=handler,
            elements=(element,),
            noise_covariance=(1, 1, 1),
        ),
        Measurement(
            time_range=TimeRange(2, 2),
            values=(4, 5, 6),
            handler=handler,
            elements=(element,),
            noise_covariance=(2, 2, 2),
        ),
        Measurement(
            time_range=TimeRange(3, 3),
            values=(7, 8, 9),
            handler=handler,
            elements=(element,),
            noise_covariance=(3, 3, 3),
        ),
    ]


def test_graph_candidate_initialization():
    graph_candidate = GraphCandidate()
    assert isinstance(graph_candidate.states, deque)
    with pytest.raises(ValueError):
        _ = graph_candidate.time_range


def test_graph_candidate_add_state():
    graph_candidate = GraphCandidate()
    state = State()
    graph_candidate.add(state)
    assert len(graph_candidate.states) == 1
    assert graph_candidate.states[0] == state


def test_graph_candidate_remove_state():
    graph_candidate = GraphCandidate()
    state = State()
    graph_candidate.add(state)
    graph_candidate.remove(state)
    assert len(graph_candidate.states) == 0


def test_graph_candidate_remove_first():
    graph_candidate = GraphCandidate()
    state1 = State()
    state2 = State()
    graph_candidate.add(state1)
    graph_candidate.add(state2)
    graph_candidate.remove_first()
    assert len(graph_candidate.states) == 1
    assert graph_candidate.states[0] == state2


def test_graph_candidate_remove_last():
    graph_candidate = GraphCandidate()
    state1 = State()
    state2 = State()
    graph_candidate.add(state1)
    graph_candidate.add(state2)
    graph_candidate.remove_last()
    assert len(graph_candidate.states) == 1
    assert graph_candidate.states[0] == state1


def test_graph_candidate_clear():
    graph_candidate = GraphCandidate()
    state = State()
    graph_candidate.add(state)
    graph_candidate.clear()
    assert len(graph_candidate.states) == 0
    with pytest.raises(ValueError):
        _ = graph_candidate.time_range


def test_graph_candidate_update_time_range(measurements):
    graph_candidate = GraphCandidate()
    state1 = State()
    state1.add(measurements[0])
    state2 = State()
    state2.add(measurements[1])
    state3 = State()
    state3.add(measurements[2])

    graph_candidate.add(state1)
    graph_candidate.add(state2)
    graph_candidate.add(state3)

    assert graph_candidate.time_range.start == 1
    assert graph_candidate.time_range.stop == 3
