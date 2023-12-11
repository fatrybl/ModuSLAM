from abc import ABC, abstractmethod

from slam.frontend_manager.elements_distributor.elements_distributor import MeasurementStorage


class StateAnalyzer(ABC):
    """
    Analyzes processed measurements and decides whether to add a new state.
    """

    def __init__(self) -> None:
        self.new_state_status: bool = False

    @abstractmethod
    def evaluate(self, storage: MeasurementStorage) -> None:
        """
        Decides whether to add a new state based on current MeasurementStorage
        """


class LidarStateAnalyzer(StateAnalyzer):
    def __init__(self) -> None:
        super().__init__()
        self.num_pointclouds = 1

    def evaluate(self, storage: MeasurementStorage) -> None:
        """
        Analyzes the storage. Seeks for a measurement obtained with the point-cloud registration handler.
        If found, changes the new_state_status flag.
        Args:
            storage: a storage with the processed measurements from handlers
        """
        pointcloud_measurements = storage.data[ScanMatching]
        num_measurements = len(pointcloud_measurements)
        if num_measurements == self.num_pointclouds:
            self.new_state_status = True
