import logging
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from data_manager.batch_factory.batch_factory import BatchFactory
from data_manager.chunk_factory.chunk_factory import ChunkFactory, DataChunk
from data_manager.data_filter.raw_data_filter import RawDataFilter
from pathlib2 import Path
import glob


class DataManager():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.config = Config(ConfigFilePaths.data_manager_config)
        self.__data_files_dir = Path(self.config.attributes.data_dir)
        self.batch_factory = BatchFactory()
        self.chunk_factory = ChunkFactory()
        if self.__config.attributes.use_filter:
            self.data_filter = RawDataFilter()

    def __sort_files(self) -> list:
        if self.config.attributes.data_files_sort_type == 'name':
            pass
        if self.config.attributes.data_files_sort_type == 'date':
            pass
        files = sorted(filter(Path.is_file, glob.glob(self.__data_files_dir + '*')))
        return files

    def __create_file_list(self) -> None:
        self.batch_factory.data_files = self.__sort_files()


    def make_chunk(self) -> DataChunk:
        if not self.batch_factory.batch.exist():
            self.batch_factory.create()
            if self.data_filter:
                self.data_filter.filter(self.batch_factory.batch)

        self.chunk_factory.create(self.batch_factory.batch)

        return self.chunk_factory.chunk
