import logging

from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.logger.logging_config import setup_manager_logger
from slam.system_configs.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)
from slam.utils.auxiliary_methods import import_object
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(setup_manager_logger)


class StateAnalyzersFactory:
    """Creates and stores state analyzers."""

    _analyzers = set[StateAnalyzer]()
    _analyzers_dict = dict[str, StateAnalyzer]()

    @classmethod
    def get_analyzers(cls) -> set[StateAnalyzer]:
        """Gets all state analyzers."""
        return cls._analyzers

    @classmethod
    def init_analyzers(cls, config: StateAnalyzersFactoryConfig) -> None:
        """Initializes state analyzers for the given configuration by importing
        corresponding modules, objects and creating instances.

        Args:
            config: configuration for state analyzers.
        """
        cls._analyzers.clear()
        cls._analyzers_dict.clear()

        package_name: str = config.package_name

        for name, cfg in config.analyzers.items():
            module_name: str = cfg.module_name
            analyzer_object: type[StateAnalyzer] = import_object(
                cfg.type_name, module_name, package_name
            )
            new_analyzer: StateAnalyzer = analyzer_object(cfg)
            cls._analyzers.add(new_analyzer)
            cls._analyzers_dict[name] = new_analyzer

    @classmethod
    def get_analyzer(cls, analyzer_name: str) -> StateAnalyzer:
        """Gets state analyzer with the given name.

        Args:
            analyzer_name: name of a state analyzer.

        Returns:
            state analyzer.

        Raises:
            ItemNotFoundError: if no analyzer with the given name is found.
        """
        try:
            return cls._analyzers_dict[analyzer_name]
        except KeyError:
            msg = f"No analyzer with name {analyzer_name!r} in {cls._analyzers}"
            logger.critical(msg)
            raise ItemNotFoundError(msg)
