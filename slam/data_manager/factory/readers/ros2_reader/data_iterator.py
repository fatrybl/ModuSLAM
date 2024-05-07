from dataclasses import dataclass, field


@dataclass
class Iterator:
    """Iterator for the sensor`s timestamp file."""

    file: str
    position: int = 0
    iterator: iter = field(init=False)

    def reset(self):
        self.position = 0
        self.__post_init__()

    def __post_init__(self):
        f = open(self.file, "r")
        self.iterator = iter(f)

    def __next__(self):
        try:
            values = next(self.iterator)
            self.position += 1
            return values
        except StopIteration:
            raise

    def __iter__(self):
        return self.iterator