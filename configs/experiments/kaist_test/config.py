from dataclasses import dataclass, field

from configs.experiments.kaist.config import Kaist, KaistDM
from configs.system.data_manager.manager import DataManager
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.setup_manager.setup import SensorConfig, SetupManager
from slam.setup_manager.sensor_factory.sensors import Imu

imu = SensorConfig('xsens_imu', Imu.__name__, 'imu.yaml')


@dataclass
class Sensors(SetupManager):
    all_sensors: list[SensorConfig] = field(
        default_factory=lambda: [imu])

    used_sensors: list[SensorConfig] = field(
        default_factory=lambda: [imu])


@dataclass
class TestMA(MemoryAnalyzer):
    graph_memory: float = 10


@dataclass
class TestDM(KaistDM):
    memory: MemoryAnalyzer = field(default_factory=TestMA)


@dataclass
class TestKaist(Kaist):
    setup_manager: SetupManager = field(default_factory=Sensors)
    data_manager: DataManager = field(default_factory=TestDM)
