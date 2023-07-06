from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from pathlib2 import Path
from yaml import safe_load


class Config:
    def __init__(self, file: ConfigFilePaths, object: object = None) -> None:
        self.file_path = file.value
        self.file_name = self.file_path.name
        self.file_type = self.file_path.suffix
        self.owner = object
        if Config.is_valid():
            self.__from_file()

    @classmethod
    def is_valid(cls) -> bool:
        """
        1) check if file exists in configs directory
        2) check if file type is valid
        3) check if file is not empty
        """
        return True

    def __from_file(self):
        with open(self.file_path, "r") as f:
            self.attributes = safe_load(f)

    def to_file() -> None:
        raise NotImplementedError
