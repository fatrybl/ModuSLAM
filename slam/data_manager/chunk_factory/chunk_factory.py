import logging
from data_chunk import DataChunk 

class ChunkFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__chunk = DataChunk

    @property
    def chunk(self) -> DataChunk:
        return self.__chunk
    
    @chunk.setter
    def chunk(self, data:SomeDataType) -> None:
        self.chunk = data