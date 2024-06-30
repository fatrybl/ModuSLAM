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
# f4 = data_dir / "1544676777318211000.bin"
# f5 = data_dir / "1544676777419059000.bin"
# f6 = data_dir / "1544676777519918000.bin"
# f7 = data_dir / "1544676777620763000.bin"
# f8 = data_dir / "1544676777721613000.bin"
# f9 = data_dir / "1544676777822490000.bin"
# f10 = data_dir / "1544676777923340000.bin"

pc1 = read_binary(f1)
pc2 = read_binary(f2)
pc3 = read_binary(f3)
# pc4 = read_binary(f4)
# pc5 = read_binary(f5)
# pc6 = read_binary(f6)
# pc7 = read_binary(f7)
# pc8 = read_binary(f8)
# pc9 = read_binary(f9)
# pc10 = read_binary(f10)

m1 = RawMeasurement(sensor=sensor, values=pc1)
loc1 = BinaryDataLocation(f1)
el1 = Element(timestamp=1544676777015627000, measurement=m1, location=loc1)

m2 = RawMeasurement(sensor=sensor, values=pc2)
loc2 = BinaryDataLocation(f2)
el2 = Element(timestamp=1544676777116478000, measurement=m2, location=loc2)

m3 = RawMeasurement(sensor=sensor, values=pc3)
loc3 = BinaryDataLocation(f3)
el3 = Element(timestamp=1544676777217336000, measurement=m3, location=loc3)

# commented out because they are not used in the tests.

# m4 = RawMeasurement(sensor=sensor, values=pc4)
# loc4 = BinaryDataLocation(f4)
# el4 = Element(timestamp=1544676740101488000, measurement=m4, location=loc4)
#
# m5 = RawMeasurement(sensor=sensor, values=pc5)
# loc5 = BinaryDataLocation(f5)
# el5 = Element(timestamp=1544676740202342000, measurement=m5, location=loc5)
#
# m6 = RawMeasurement(sensor=sensor, values=pc6)
# loc6 = BinaryDataLocation(f6)
# el6 = Element(timestamp=1544676740303223000, measurement=m6, location=loc6)
#
# m7 = RawMeasurement(sensor=sensor, values=pc7)
# loc7 = BinaryDataLocation(f7)
# el7 = Element(timestamp=1544676740404102000, measurement=m7, location=loc7)
#
# m8 = RawMeasurement(sensor=sensor, values=pc8)
# loc8 = BinaryDataLocation(f8)
# el8 = Element(timestamp=1544676740504911000, measurement=m8, location=loc8)
#
# m9 = RawMeasurement(sensor=sensor, values=pc9)
# loc9 = BinaryDataLocation(f9)
# el9 = Element(timestamp=1544676740605762000, measurement=m9, location=loc9)
#
# m10 = RawMeasurement(sensor=sensor, values=pc10)
# loc10 = BinaryDataLocation(f10)
# el10 = Element(timestamp=1544676740706642000, measurement=m10, location=loc10)

scenarios = (([el1], None), ((el1, el2), Measurement), ((el2, el3), Measurement))
