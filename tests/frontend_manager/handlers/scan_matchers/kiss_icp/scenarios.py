import numpy as np
import numpy.typing as npt

from slam.data_manager.factory.element import Element
from slam.data_manager.factory.element import Measurement as RawMeasurement
from slam.data_manager.factory.readers.kaist.auxiliary_classes import BinaryDataLocation
from slam.data_manager.factory.readers.kaist.measurement_collector import (
    MeasurementCollector,
)
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.setup_manager.sensors_factory import SensorConfig
from tests_data import current_directory

tests_data_dir = current_directory
data_dir = tests_data_dir / "kaist_urban30_gangnam/VLP_left"

f1 = data_dir / "1544676777015627000.bin"
f2 = data_dir / "1544676777116478000.bin"
f3 = data_dir / "1544676777217336000.bin"
f4 = data_dir / "1544676777318211000.bin"
f5 = data_dir / "1544676777419059000.bin"
f6 = data_dir / "1544676777519918000.bin"
f7 = data_dir / "1544676777620763000.bin"
f8 = data_dir / "1544676777721613000.bin"
f9 = data_dir / "1544676777822490000.bin"
f10 = data_dir / "1544676777923340000.bin"

pc1: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f1)
pc2: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f2)
pc3: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f3)
pc4: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f4)
pc5: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f5)
pc6: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f6)
pc7: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f7)
pc8: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f8)
pc9: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f9)
pc10: npt.NDArray[np.float32] = MeasurementCollector.read_bin(f10)


s1 = Sensor(config=SensorConfig(name="vlp_left", type_name="Lidar3D"))
m1 = RawMeasurement(sensor=s1, values=tuple(pc1))
loc1 = BinaryDataLocation(f1)
el1 = Element(timestamp=1544676739798931000, measurement=m1, location=loc1)

m2 = RawMeasurement(sensor=s1, values=tuple(pc2))
loc2 = BinaryDataLocation(f2)
el2 = Element(timestamp=1544676739899753000, measurement=m2, location=loc2)

m3 = RawMeasurement(sensor=s1, values=tuple(pc3))
loc3 = BinaryDataLocation(f3)
el3 = Element(timestamp=1544676740000631000, measurement=m3, location=loc3)

m4 = RawMeasurement(sensor=s1, values=tuple(pc4))
loc4 = BinaryDataLocation(f4)
el4 = Element(timestamp=1544676740101488000, measurement=m4, location=loc4)

m5 = RawMeasurement(sensor=s1, values=tuple(pc5))
loc5 = BinaryDataLocation(f5)
el5 = Element(timestamp=1544676740202342000, measurement=m5, location=loc5)

m6 = RawMeasurement(sensor=s1, values=tuple(pc6))
loc6 = BinaryDataLocation(f6)
el6 = Element(timestamp=1544676740303223000, measurement=m6, location=loc6)

m7 = RawMeasurement(sensor=s1, values=tuple(pc7))
loc7 = BinaryDataLocation(f7)
el7 = Element(timestamp=1544676740404102000, measurement=m7, location=loc7)

m8 = RawMeasurement(sensor=s1, values=tuple(pc8))
loc8 = BinaryDataLocation(f8)
el8 = Element(timestamp=1544676740504911000, measurement=m8, location=loc8)

m9 = RawMeasurement(sensor=s1, values=tuple(pc9))
loc9 = BinaryDataLocation(f9)
el9 = Element(timestamp=1544676740605762000, measurement=m9, location=loc9)

m10 = RawMeasurement(sensor=s1, values=tuple(pc10))
loc10 = BinaryDataLocation(f10)
el10 = Element(timestamp=1544676740706642000, measurement=m10, location=loc10)

res1 = None

scenarios = ((el1, res1),)
