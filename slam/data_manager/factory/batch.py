import pandas as pd
from data_manager.factory.readers.data_reader import Element

class DataBatch:
    def __init__(self):
        self.__data = {"time": [],
                       "message": [],
                       "position": [], }

    def add(self, new_element: Element):
        self.__data["time"].append(new_element.time)
        self.__data["message"].append(new_element.message)
        self.__data["time"].append(new_element.position)

    def to_dataframe(self,) -> None:
        self.__data = pd.DataFrame.from_dict(self.__data)

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def size_bytes(self) -> int:
        return self.__data.memory_usage(deep=True, index=True).sum()

    def exist(self) -> bool:
        if self.__data["time"]:
            return True
        else:
            return False
