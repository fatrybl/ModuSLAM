import pandas as pd
from slam.data_manager.factory.readers.element_factory import Data, Element


class DataBatch:
    def __init__(self):
        self.__data = Data()
        self.__margin_location = None

    def add(self, new_element: Element) -> None:
        self.__data.timestamps.append(new_element.timestamp)
        self.__data.measurements.append(new_element.measurement)
        self.__data.locations.append(new_element.location)

    def to_dataframe(self,) -> None:
        self.__data = pd.DataFrame.from_dict(self.__data)

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def size_bytes(self) -> int:
        return self.__data.memory_usage(deep=True, index=True).sum()

    # @property
    # def margin_location(self) -> Location:
    #     return self._margin_location
