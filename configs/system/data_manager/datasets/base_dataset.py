from dataclasses import dataclass


@dataclass
class Dataset:
    type: str
    directory: str
