import DataLoader, RawDataFilter, MeasurementsSynchronizer, ConfigManager, FactorsCreator, BatchSolver, MapSaver
"""
Main class to handle the mapping system.
"""
class SystemManager:
    def __init__(self):
        self.Data_Loader = DataLoader()
        self.Data_Filter = RawDataFilter()
        self.Synchronizer = MeasurementsSynchronizer()
        self.Factor_Creator = FactorsCreator()
        self.Solver = BatchSolver
        self.Map = MapSaver

    def build_map():
        while isDataAvailable:
            self.Data_Loader.get_data()
            self.Data_Filter.filter_data()

            while isDataBatchAvailable:
                self.Synchronizer.sync_data()
                self.Factor_Creator.make_factors()
                self.Solver.solve()

            self.Map.save()