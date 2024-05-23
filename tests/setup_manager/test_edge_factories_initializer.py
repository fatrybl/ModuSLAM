"""Tests for the EdgeFactoriesInitializer class."""

from unittest.mock import MagicMock, patch

from slam.frontend_manager.edge_factories.lidar_odometry import LidarOdometryEdgeFactory
from slam.setup_manager.edge_factories_initializer import factory as factory_module
from slam.setup_manager.edge_factories_initializer.factory import (
    EdgeFactoriesInitializer,
)
from slam.system_configs.setup_manager.edge_factories_initializer import (
    EdgeFactoriesInitializerConfig,
)


def test_init_factories():
    # Mock the EdgeFactoryConfig
    mock_factory_config = MagicMock()
    mock_factory_config.name = "mock_test_factory"
    mock_factory_config.type_name = "mock_type_name"
    mock_factory_config.module_name = "mock_module_name"

    # Mock the EdgeFactoriesInitializerConfig
    mock_config = MagicMock(spec=EdgeFactoriesInitializerConfig)
    mock_config.package_name = "mock_package_name"
    mock_config.edge_factories = {mock_factory_config.name: mock_factory_config}

    with patch.object(factory_module, "import_object") as mock_import_object:
        mock_import_object.return_value = LidarOdometryEdgeFactory

        EdgeFactoriesInitializer.init_factories(mock_config)
        factory = EdgeFactoriesInitializer.get_factory(mock_factory_config.name)

        # Assert the import_object was called with correct arguments
        mock_import_object.assert_called_once_with(
            mock_factory_config.type_name, mock_factory_config.module_name, mock_config.package_name
        )

        assert isinstance(factory, LidarOdometryEdgeFactory)
