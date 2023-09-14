from slam.data_manager.factory.readers.element_factory import Element


class DataBatch:
    def __init__(self):
        self.__data: list[Element] = []
        self.__margin_location = None

    def add(self, new_element: Element) -> None:
        self.__data.append(new_element)

    @property
    def data(self) -> list[Element]:
        return self.__data

    @property
    def size_bytes(self) -> int:
        return self.__data.memory_usage(deep=True, index=True).sum()

    # @property
    # def margin_location(self) -> Location:
    #     return self._margin_location
