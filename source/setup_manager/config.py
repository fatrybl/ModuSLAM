class Config:
    def __init__(self, filename, object=None) -> None:
        self.file_name = filename
        self.object = object
        self.file_path = DEFAULT_PATH + self.file_name
        self.file_type = self.file_path.suffix()
        if self.is_valid():
            self.attributes = self.from_file()

    def is_valid(self) -> bool:
        """
        1) check if file exists in configs directory
        2) check if file type is valid
        3) check if file is not empty
        """
        return False

    def from_file() -> None:
        pass

    def to_file() -> None:
        pass