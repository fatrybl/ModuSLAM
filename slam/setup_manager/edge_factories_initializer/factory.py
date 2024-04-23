import logging

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.system_configs.system.setup_manager.edge_factories_initializer import (
    EdgeFactoriesInitializerConfig,
)
from slam.utils.auxiliary_methods import import_object

logger = logging.getLogger(__name__)


class EdgeFactoriesInitializer:
    """Distributes edge factories."""

    _factories = set[EdgeFactory]()

    @classmethod
    def get_all_factories(cls) -> set[EdgeFactory]:
        """Returns all edge factories.

        Returns:
            (set[EdgeFactory]): all edge factories.
        """
        return cls._factories

    @classmethod
    def get_factory(cls, name: str) -> EdgeFactory:
        """Returns edge factory by name.

        Args:
            name (str): name of the factory.

        Returns:
            (EdgeFactory): edge factory.
        """
        for factory in cls._factories:
            if factory.name == name:
                return factory

        msg = f"Edge factory with name {name!r} has not been found in {cls._factories}."
        logger.error(msg)
        raise ValueError(msg)

    @classmethod
    def init_factories(cls, config: EdgeFactoriesInitializerConfig) -> None:
        package_name: str = config.package_name

        for cfg in config.edge_factories.values():
            factory_object: type[EdgeFactory] = import_object(
                cfg.type_name, cfg.module_name, package_name
            )
            new_factory: EdgeFactory = factory_object(cfg)
            cls._factories.add(new_factory)
