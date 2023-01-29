"""
This class synchronize data from different sensors.
It estimates the timestamp of the next vertex (state) in graph based on timestamps and current dynamics
"""
# import sys
# sys.path.insert(0,"../../..")
from src.data_manager.data_reader.DataLoader import DataLoader

class MeasurementsSynchronizer:
    def __init__(self, data_list):
        self.CurrentTime = min([min(data) for data in data_list])
        assert self.CurrentTime >= 0
        self.MaxTravelError = None
        self.TimeStep = None
        self.MeasurementsList = data_list
        self.CurrentState = None
        self.isSystemInitialized = False
        self.isDataSynchronized = True
        self.FreshData = None

    def start_sync(self):
        if not self.isSystemInitialized:
            init_synchronizer()
            self.isSystemInitialized = True

        if self.isDataSynchronized:
            self.FreshData = DataLoader.get_data()
            self.isDataSynchronized = False

    def sync_measurements(self):
        NextTime = self.CurrentTime + self.TimeStep
        for data in self.MeasurementsList:
            for item in data:
                dt = min(abs(item.time - self.CurrentTime), abs(NextTime - item.time))

        self.update_current_state()
        self.update_current_time()

    def get_current_state(self) -> object:
        pass
    def get_current_time(self) -> int:
        pass
    def estimate_state(self,):
        x0 = self.CurrentState
        x1 = x0 + V0*dt
        pass
    def sort_measurements(self):
        for data in self.MeasurementsList:
            data.sort(key='timestamp')
    def update_current_state(self, state):
        pass
    def update_current_time(self):
        pass
    def link_measurement(self,measurement, vertex):
        pass
    def make_data_batch(self):
        DataBatch = []
        for data in self.MeasurementsList:
            for item in data:
                if item.time < self.CurrentTime + self.TimeStep:
                    DataBatch.append(item)
                else:
                    continue
