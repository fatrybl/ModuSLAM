"""Tests for the GraphBuilderFactory class."""

import pytest

from moduslam.frontend_manager.graph_builder.builders.pointcloud_map_builder import (
    PointcloudMapBuilder,
)
from moduslam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from moduslam.frontend_manager.graph_builder.graph_builder_factory import (
    GraphBuilderFactory,
)


@pytest.mark.parametrize(
    "name, graph_builder_type",
    [
        (PointcloudMapBuilder.__name__, PointcloudMapBuilder),
        # Add more tuples for additional test cases
    ],
)
def test_create(name: str, graph_builder_type: type[GraphBuilder]) -> None:
    result = GraphBuilderFactory.create(name)
    assert result == graph_builder_type


def test_create_invalid_builder():
    with pytest.raises(NotImplementedError):
        GraphBuilderFactory.create("InvalidBuilder")
