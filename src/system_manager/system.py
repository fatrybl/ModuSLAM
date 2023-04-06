import DataLoader, RawDataFilter, MeasurementsSynchronizer, ConfigManager, FactorsCreator, BatchSolver, MapSaver
"""
Main class to handle the mapping system.
"""
class SystemManager:
    def __init__(self):
        self.Data_Loader = DataLoader()
        self.Raw_Data_Filter = RawDataFilter()
        self.Synchronizer = MeasurementsSynchronizer()
        self.Factor_Creator = FactorsCreator()
        self.Config_Manager = ConfigManager()
        self.Solver = BatchSolver
        self.Map = MapSaver

    def init_system(self):
        self.Config_Manager.process_configs()
        self.Solver.init_graphs()
        #TODO: maybe init some extra modules...

    def build_map(self,):
        while self.Data_Loader.isDataAvailable:
            self.Data_Loader.get_data()
            self.Raw_Data_Filter.filter_data()

            while self.Synchronizer.isUnprocessedDataBatchLeft:
                self.Synchronizer.sync_data()
                self.Factor_Creator.make_factors()
                self.Solver.solve()
                self.Synchronizer.update()

            self.Data_Loader.update_status()
            self.Map.save()