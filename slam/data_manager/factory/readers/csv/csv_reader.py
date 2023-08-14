import logging

from pathlib import Path

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from readers.data_reader import DataReader

class CsvReader(DataReader):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.__params = Config(ConfigFilePaths.data_reader_config).attributes["csv_reader"]
        self.__newline = self.__params["new_line"]
        self.__delimiter = self.__params["delimiter"]
        self.__quotechar = self.__params["quotechar"]
        self.__messages = self.__params["messages"]
        # self._file_name = file_path.stem
        # self._file_type = file_path.suffix
        # self._file_size = file_path.stat().st_size
        # self._is_file_processed = False
        # self._current_position = 0

    def get_elements(self) -> list[Element]:
        self.check_file(file_path)
        with open(file_path, 'r',  newline=self.__newline) as f:
            reader = csv.reader(f,
                                delimiter=self.__delimiter,
                                quotechar=self.__quotechar)
            row = next(reader)
            row = {x: row[x] for x in self.__used_topic_names}
            self._element_factory.row_to_elements(row)
            self._current_position = reader.line_num

        return self._element_factory.elements