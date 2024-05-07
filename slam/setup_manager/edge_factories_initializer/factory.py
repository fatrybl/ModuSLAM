import logging

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.logger.logging_config import setup_manager
from slam.system_configs.setup_manager.edge_factories_initializer import (
    EdgeFactoriesInitializerConfig,
)
from slam.utils.auxiliary_methods import import_object

logger = logging.getLogger(setup_manager)


class EdgeFactoriesInitializer:
    """Creates and stores edge factories."""

    _factories = set[EdgeFactory]()

    @classmethod
    def get_all_factories(cls) -> set[EdgeFactory]:
        """Gets all edge factories."""
        return cls._factories

    @classmethod
    def get_factory(cls, name: str) -> EdgeFactory:
        """Gets edge factory with the given name.

        Args:
            name: name of a factory.

        Returns:
            edge factory.

        Raises:
            ValueError: if factory with the given name has not been found.
        """
        for factory in cls._factories:
            if factory.name == name:
                return factory

        msg = f"Edge factory with name {name!r} has not been found in {cls._factories}."
        logger.error(msg)
        raise ValueError(msg)

    @classmethod
    def init_factories(cls, config: EdgeFactoriesInitializerConfig) -> None:
        """Initializes edge factories for the given configuration by importing
        corresponding modules, objects and creating instances.

        Args:
            config: configuration of edge factories.
        """
        cls._factories.clear()

        package_name: str = config.package_name

        for cfg in config.edge_factories.values():
            factory_object: type[EdgeFactory] = import_object(
                cfg.type_name, cfg.module_name, package_name
            )
            new_factory: EdgeFactory = factory_object(cfg)
            cls._factories.add(new_factory)
