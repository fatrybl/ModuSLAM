import logging

class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.memory_analyzer = MemoryAnalyzer()
        self.batch_creator = BatchCreator()
        self.chunk_provider = ChunkProvider()
        self.raw_data_filter = DataFilter()
        self._data_batch = None
        self._data_chunk = None

    @property
    def data_batch():
        pass

    @data_batch.setter
    def data_batch(self, data_batch):
        self._data_batch = data_batch

    @property
    def data_chunk():
        pass
    
    @data_chunk.setter
    def data_chunk(self, data_chunk):
        self._data_chunk = data_chunk
    
    def make_data_chunk(self) -> DataChunk:
        if not self._data_batch:
            try:
                self._data_batch = self.batch_creator.load_batch()
            except Exception as e:
                print(e)

        data_chunk = self.chunk_provider.make_chunk(self._data_batch)
        self.raw_data_filter.filter(data_chunk)  

        return data_chunk
