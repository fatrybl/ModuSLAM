from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.setup_manager.sensor_factory import Sensor

@dataclass
class RosSensorConfig():
    sensor: Sensor = MISSING
    topic: str = MISSING
    
@dataclass
class Ros1(Dataset):
    """
    Base parameters for any Ros 1 dataset.
    """
    dataset_type: str = 'Ros1'
    deserialize_raw_data: bool  = MISSING
    used_sensors: list[RosSensorConfig] = MISSING
    name: str = "ros1"
    url: str = "https://smth"
    type: str = "first"
