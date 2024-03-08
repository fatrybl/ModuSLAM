import logging

from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.system_configs.system.setup_manager.state_analyzers_factory import (
    StateAnalyzerFactoryConfig,
)
from slam.utils.auxiliary_methods import import_object
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(__name__)


class StateAnalyzerFactory:
    """Creates state analyzers."""

    _analyzers = set[StateAnalyzer]()
    _analyzers_dict = dict[str, StateAnalyzer]()

    @property
    def analyzers(self) -> set[StateAnalyzer]:
        """All analyzers.

        Returns:
            (set[StateAnalyzer]): set of analyzers.
        """
        return self._analyzers

    @classmethod
    def init_analyzers(cls, config: StateAnalyzerFactoryConfig) -> None:
        """Initializes analyzers with the given config.

        Args:
            config: configuration.
        """
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
        """
        The analyzer with the given name.
        Args:
            analyzer_name (str): name of analyzer.

        Returns:
            (StateAnalyzer): analyzer.
        """
        try:
            return cls._analyzers_dict[analyzer_name]
        except KeyError:
            msg = f"No analyzer with name {analyzer_name!r} in {cls._analyzers}"
            logger.critical(msg)
            raise ItemNotFoundError(msg)
