import logging
from data_chunk import DataChunk
from data_batch import DataBatch


class ChunkFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__chunk = DataChunk
        self.__criteria = None

    @property
    def chunk(self) -> DataChunk:
        return self.__chunk

    def __delete_element_from_batch(self) -> None:
        pass

    def __get_element_from_batch(self) -> SomeType:
        pass

    def create(self, batch: DataBatch):
        while self.__criteria:
            self.__chunk += self.__get_element_from_batch(batch)
            self.__delete_element_from_batch(batch)
