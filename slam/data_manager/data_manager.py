import logging
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from data_manager.batch_factory.batch_factory import BatchFactory
from data_manager.chunk_factory.chunk_factory import ChunkFactory, DataChunk
from data_manager.data_filter.raw_data_filter import RawDataFilter


class DataManager():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.batch_factory = BatchFactory()
        self.chunk_factory = ChunkFactory()

    def setup(self):
        cfg = Config(ConfigFilePaths.data_manager_config)
        if cfg.attributes.use_filter:
            self.data_filter = RawDataFilter()

    def make_chunk(self) -> DataChunk:
        if not self.batch_factory.batch.exist():
            self.batch_factory.create()

        if self.data_filter:
            self.data_filter.filter(self.batch_factory.batch)

        self.chunk_factory.create(self.batch_factory.batch)

        return self.chunk_factory.chunk
