import logging

from configs.system.setup_manager.state_analyzers_factory import (
    StateAnalyzersFactoryConfig,
)
from slam.frontend_manager.graph_builder.candidate_factory.state_analyzers.analyzer_ABC import (
    StateAnalyzer,
)
from slam.utils.auxiliary_methods import import_object
from slam.utils.exceptions import AnalyzerNotFound

logger = logging.getLogger(__name__)


class StateAnalyzerFactory:
    """Creates state analyzers."""

    _analyzers = set[StateAnalyzer]()

    @property
    def analyzers(self) -> set[StateAnalyzer]:
        """All analyzers.

        Returns:
            (set[StateAnalyzer]): set of analyzers.
        """
        return self._analyzers

    @classmethod
    def init_analyzers(cls, config: StateAnalyzersFactoryConfig) -> None:
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

    @classmethod
    def get_analyzer(cls, analyzer_name: str) -> StateAnalyzer:
        """
        Returns an analyzer with the given name.
        Args:
            analyzer_name (str): name of analyzer.

        Returns:
            (StateAnalyzer): analyzer.
        """
        for analyzer in cls._analyzers:
            if analyzer.name == analyzer_name:
                return analyzer
        msg = f"No analyzer with name {analyzer_name!r} in {cls._analyzers}"
        logger.critical(msg)
        raise AnalyzerNotFound(msg)
