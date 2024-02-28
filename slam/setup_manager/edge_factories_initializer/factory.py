import logging

from omegaconf import DictConfig

from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.utils.auxiliary_methods import import_object

logger = logging.getLogger(__name__)


class EdgeCreatorFactory:
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
    def init_factories(cls, config: DictConfig) -> None:
        module_name: str = config.module_name
        package_name: str = config.package_name

        for factory_cfg in config.factories:
            factory_object: type[EdgeFactory] = import_object(
                factory_cfg.name, module_name, package_name
            )
            new_factory: EdgeFactory = factory_object(factory_cfg)
            cls._factories.add(new_factory)
