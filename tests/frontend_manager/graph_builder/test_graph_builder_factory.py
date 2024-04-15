"""Tests for the GraphBuilderFactory class."""

import pytest

from slam.frontend_manager.graph_builder.builders.lidar_map_builder import (
    LidarMapBuilder,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.graph_builder_factory import (
    GraphBuilderFactory,
)


@pytest.mark.parametrize(
    "name, graph_builder_type",
    [
        (LidarMapBuilder.__name__, LidarMapBuilder),
        # Add more tuples for additional test cases
    ],
)
def test_create(name: str, graph_builder_type: type[GraphBuilder]) -> None:
    result = GraphBuilderFactory.create(name)
    assert result == graph_builder_type


def test_create_invalid_builder():
    with pytest.raises(NotImplementedError):
        GraphBuilderFactory.create("InvalidBuilder")
