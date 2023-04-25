from somewhere import DEFAULT_FILE_NAMES, DEFAULT_PATH

class SetupManager:
    def __init__(self) -> None:
        pass

class Config:
    def __init__(self, object) -> None:
        self.entity = object
        self.file_name = [name for name in DEFAULT_FILE_NAMES if name == object.type]
        self.file_path = DEFAULT_PATH + self.file_name
        self.file_type = self.file_path.suffix()
        if self.is_valid():
            self.attributes = self.from_file()

    def is_valid() -> bool:
        pass

    def from_file() -> None:
        pass

    def to_file() -> None:
        pass

class InitObject:
    def __init__(self) -> None:
        pass