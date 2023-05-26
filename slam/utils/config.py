from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from pathlib2 import Path

class Config:
    def __init__(self, file: ConfigFilePaths, object:object=None) -> None:
        self.file_path = Path(file.value)
        self.file_name = self.file_path.name
        self.file_type = self.file_path.suffix
        self.object = object
        if Config.is_valid():
            self.attributes = self.__from_file()
        
    
    @classmethod
    def is_valid(cls) -> bool:
        """
        1) check if file exists in configs directory
        2) check if file type is valid
        3) check if file is not empty
        """
        return False

    def __from_file(self) -> None:
        pass

    def to_file() -> None:
        pass