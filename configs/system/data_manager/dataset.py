from dataclasses import dataclass, field


@dataclass
class Dataset:
    type: str
    directory: str
    time_limit: list[int] = field(
        metadata={'timestamp limits': 'list of 2 integers: [start, stop]'})
