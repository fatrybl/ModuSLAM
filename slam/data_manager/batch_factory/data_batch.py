import pandas as pd


class DataBatch:
    def __init__(self):
        self.__data = pd.DataFrame(columns=['time', 'sensor', 'data'])

    @property
    def data(self) -> pd.DataFrame:
        return self.__data
    
    @property
    def size_bytes(self) -> int:
        return self.__data.memory_usage(deep=True, index=True).sum()
    
    def exist(self):
        """Check if any data is available in dataframe"""
        pass