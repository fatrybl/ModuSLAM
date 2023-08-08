import logging

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from yaml import safe_load

logger = logging.getLogger(__name__)


class Config:
    def __init__(self, file: ConfigFilePaths):
        self.file_path = file.value
        self.file_name = self.file_path.name
        self.file_type = self.file_path.suffix
        if self.__is_valid():
            self.__read_file()

    def __is_valid(self) -> bool:
        if not self.file_path.exists():
            logger.critical(f"File {self.file_path} does not exist")
            return False

        if self.file_type != ".yaml":
            logger.critical(f"File type of {self.file_type} is not valid")
            return False

        if self.file_path.stat().st_size == 0:
            logger.critical(f"File {self.file_path} is empty")
            return False

        return True

    def __read_file(self):
        with open(self.file_path, "r") as f:
            self.attributes = safe_load(f)

    def to_file() -> None:
        raise NotImplementedError
