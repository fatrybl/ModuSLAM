import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class GraphBuilder(ABC):
    """
    Base graph factory to create a sub-graph from the processed measurements and
    merge it with the main graph.
    """

    @abstractmethod
    def graph_candidate_ready(self) -> bool:
        """
        Indicates if a sub-graph has been created based on criteria.

        Returns:
            bool: success or failure status.
        """

    @abstractmethod
    def process_storage(self, storage: Any) -> None:
        """
        Processes a measurement s.t.

        Args:
            m (_type_): latest element[Element] from a Data Batch processed with the corresponding external module.
            measurements (_type_): dictionary of measurements from Distributor object.

        1) Analyze the measurements whether to create new sub-graph[Graph]
        2) If new sub-graph: add factors
        3) If sub-graph ready: change status.
        """
