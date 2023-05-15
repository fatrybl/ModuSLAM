class DataManagerParameters(ObjectParameters):
    def __init__(self) -> None:
        super().__init__()

        self.batch_factory = BatchFactoryParameters()
        self.chunk_factory = ChunkFactoryParameters()
        self.memory_analyzer = MemoryAnalyzerParameters()
        self.data_filter = DataFilterParameters()