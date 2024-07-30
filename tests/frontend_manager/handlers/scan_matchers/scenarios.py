from moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from moduslam.data_manager.batch_factory.readers.kaist.utils import read_binary
from moduslam.data_manager.batch_factory.readers.locations import BinaryDataLocation
from moduslam.frontend_manager.measurement_storage import Measurement
from moduslam.setup_manager.sensors_factory.sensors import Lidar3D
from moduslam.system_configs.setup_manager.sensors import Lidar3DConfig
from tests.conftest import kaist_urban30_dataset_dir

data_dir = kaist_urban30_dataset_dir / "VLP_left"

sensor = Lidar3D(config=Lidar3DConfig(name="vlp_left"))

f1 = data_dir / "1544676777015627000.bin"
f2 = data_dir / "1544676777116478000.bin"
f3 = data_dir / "1544676777217336000.bin"

pc1 = read_binary(f1)
pc2 = read_binary(f2)
pc3 = read_binary(f3)

m1 = RawMeasurement(sensor=sensor, values=pc1)
loc1 = BinaryDataLocation(f1)
el1 = Element(timestamp=1544676777015627000, measurement=m1, location=loc1)

m2 = RawMeasurement(sensor=sensor, values=pc2)
loc2 = BinaryDataLocation(f2)
el2 = Element(timestamp=1544676777116478000, measurement=m2, location=loc2)

m3 = RawMeasurement(sensor=sensor, values=pc3)
loc3 = BinaryDataLocation(f3)
el3 = Element(timestamp=1544676777217336000, measurement=m3, location=loc3)


scenarios = (([el1], None), ((el1, el2), Measurement), ((el2, el3), Measurement))
