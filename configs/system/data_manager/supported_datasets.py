from abc import ABC
from dataclasses import dataclass


@dataclass
class Dataset(ABC):
    """Base class for any supported dataset"""
    name: str
    url: str


class Kaist(Dataset):
    name: str = "Kaist Urban Dataset"
    url: str = "https://sites.google.com/view/complex-urban-dataset"


class Ros1(Dataset):
    """Any Ros1 based dataset"""
