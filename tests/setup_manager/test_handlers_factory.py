"""Tests for the HandlersFactory class."""

from unittest.mock import MagicMock, patch

from slam.frontend_manager.handlers.pointcloud_matcher import ScanMatcher
from slam.setup_manager.handlers_factory import factory as factory_module
from slam.setup_manager.handlers_factory.factory import HandlersFactory
from slam.system_configs.system.setup_manager.handlers_factory import (
    HandlersFactoryConfig,
)


def test_init_handlers():
    # Mock the HandlerConfig
    mock_handler_config = MagicMock()
    mock_handler_config.name = "mock_test_handler"
    mock_handler_config.type_name = "mock_type_name"
    mock_handler_config.module_name = "mock_module_name"

    # Mock the HandlersFactoryConfig
    mock_config = MagicMock(spec=HandlersFactoryConfig)
    mock_config.package_name = "mock_package_name"
    mock_config.handlers = {mock_handler_config.name: mock_handler_config}

    with patch.object(factory_module, "import_object") as mock_import_object:
        mock_import_object.return_value = ScanMatcher

        HandlersFactory.init_handlers(mock_config)
        factory = HandlersFactory.get_handler(mock_handler_config.name)

        mock_import_object.assert_called_once_with(
            mock_handler_config.type_name, mock_handler_config.module_name, mock_config.package_name
        )

        assert isinstance(factory, ScanMatcher)
