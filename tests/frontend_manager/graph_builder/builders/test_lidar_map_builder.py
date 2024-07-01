"""Tests for the LidarMapBuilder class.

Build simple graph with 2 nodes (LidarPose) and 1 edge (LidarOdometry).
"""

import pytest

from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from moduslam.frontend_manager.graph.graph import Graph

from .conftest import builder, data_batch, setup_manager


def test_create_graph_candidate(data_batch, builder, setup_manager):
    el1 = data_batch.data[0]
    el2 = data_batch.data[1]

    builder.create_graph_candidate(data_batch)
    candidate = builder.graph_candidate

    assert candidate is not None
    assert len(candidate.states) == 1
    assert candidate.time_range.start == el1.timestamp
    assert candidate.time_range.stop == el2.timestamp


def test_merge_graph_candidate(data_batch, builder, setup_manager):
    builder.create_graph_candidate(data_batch)

    graph = Graph[LidarPose, LidarOdometry]()
    builder.merge_graph_candidate(graph)

    assert len(graph.vertex_storage.vertices) == 2
    assert len(graph.edge_storage.edges) == 1
    assert graph.factor_graph.nrFactors() == 1
    assert graph.gtsam_values.size() == 2


def test_create_graph_candidate_empty_batch(builder, setup_manager):
    empty_batch = DataBatch()

    builder.create_graph_candidate(empty_batch)
    candidate = builder.graph_candidate

    with pytest.raises(ValueError):
        __ = candidate.time_range  # noqa: F841

    assert len(candidate.states) == 0


def test_merge_graph_candidate_no_candidate(builder, setup_manager):
    graph = Graph[LidarPose, LidarOdometry]()
    builder.merge_graph_candidate(graph)

    assert len(graph.vertex_storage.vertices) == 0
    assert len(graph.edge_storage.edges) == 0
    assert graph.factor_graph.nrFactors() == 0
    assert graph.gtsam_values.size() == 0


def test_clear_candidate(data_batch, builder, setup_manager):
    builder.create_graph_candidate(data_batch)
    builder.clear_candidate()

    candidate = builder.graph_candidate
    assert len(candidate.states) == 0
    with pytest.raises(ValueError):
        __ = candidate.time_range  # noqa: F841
