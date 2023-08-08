import pandas as pd
from data_manager.factory.readers.data_reader import Element


class DataBatch:
    def __init__(self):
        self.__data = {"timestamp": [],
                       "measurement": [],
                       "location": [], }

    def add(self, new_element: Element) -> None:
        if new_element:
            self.__data["timestamp"].append(new_element.time)
            self.__data["measurement"].append(new_element.measurement)
            self.__data["location"].append(new_element.location)

    def to_dataframe(self,) -> None:
        self.__data = pd.DataFrame.from_dict(self.__data)

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def size_bytes(self) -> int:
        return self.__data.memory_usage(deep=True, index=True).sum()

    def exist(self) -> bool:
        if self.__data["timestamp"]:
            return True
        else:
            return False
