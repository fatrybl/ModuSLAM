from dataclasses import dataclass
from unittest.mock import patch

import pytest

from slam.frontend_manager.graph_builder.builders.lidar_submap_builder import (
    LidarMapBuilder,
)
from slam.frontend_manager.graph_builder.graph_builder_factory import (
    GraphBuilderFactory,
)


@dataclass
class TestConfig:
    name: str = LidarMapBuilder.__name__


class TestGraphBuilderFactory:
    def test_create_lidar_map_builder(self):
        with patch.object(LidarMapBuilder, "__init__", return_value=None) as mock_init:
            config = TestConfig()
            builder = GraphBuilderFactory.create(config)
            assert isinstance(builder, LidarMapBuilder)
            mock_init.assert_called_once_with(config)

    def test_create_not_supported(self):
        config = TestConfig(name="SomeFakeBuilder")
        with pytest.raises(NotImplementedError):
            GraphBuilderFactory.create(config)
