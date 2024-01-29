import logging
from abc import ABC, abstractmethod

from slam.frontend_manager.elements_distributor.elements_distributor import (
    MeasurementStorage,
)
from slam.frontend_manager.graph_builders.candidate_factory.candidate_factory import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builders.graph_merger.graph_merger import GraphMerger

logger = logging.getLogger(__name__)


class GraphBuilder(ABC):
    """
    Base graph factory to create a sub-graph from the processed measurements and
    merge it with the main graph.
    """

    @property
    @abstractmethod
    def candidate_factory(self) -> CandidateFactory:
        """
        A factory for creating a candidate to be merged with the main graph.
        Returns:
            (CandidateFactory)
        """

    @property
    @abstractmethod
    def candidate_merger(self) -> GraphMerger:
        """
        A merger for connecting graph candidate with the main graph.
        Returns:
            (GraphMerger)
        """

    @abstractmethod
    def graph_candidate_ready(self) -> bool:
        """
        Indicates if a sub-graph has been created based on criteria.

        Returns:
            (bool): success or failure status.
        """

    @abstractmethod
    def process_storage(self, storage: MeasurementStorage) -> None:
        """
        Processes a measurement s.t.

        Args:
            storage (MeasurementStorage): storage with measurements.
        """
