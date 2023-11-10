from PIL import Image
import hydra
from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module
from dataclasses import dataclass, field
from email.policy import default
from pathlib import Path
import numpy

from omegaconf import MISSING, DictConfig

# from configs.sensors.base_sensor_parameters import Parameter
from configs.sensors.imu import ImuParameter
from configs.system.setup_manager.sensor_factory import SensorConfig
from slam.data_manager.factory.batch import DataBatch

from slam.data_manager.factory.readers.element_factory import Element, Location, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import CsvDataLocation, StereoImgDataLocation
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Imu, VrsGps


# from tests.data_manager.factory.batch_factory.api.data import el19, el22, stereo_requests, stereo_batch

# db = DataBatch()
# img1 = Image.new(mode="RGB", size=(2, 2))
# img2 = Image.new(mode="RGB", size=(2, 2))

# el1: Element = Element(timestamp=1,
#                        measurement=Measurement(
#                            sensor=Imu(
#                                name='imu',
#                                config=DictConfig({"pose": [1, 2, 3]})),
#                            values=(img1, img2)),
#                        location=StereoImgDataLocation(files=(Path(), Path())))

# el2: Element = Element(timestamp=1,
#                        measurement=Measurement(
#                            sensor=Imu(
#                                name='imu',
#                                config=DictConfig({"pose": [1, 2, 3]})),
#                            values=(img1, img2)),
#                        location=StereoImgDataLocation(files=(Path(), Path())))
# test_set = DataBatch()
# test_set.add(el1)
# test_set.add(el2)
# print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
# print(len(test_set.data))
# # elements: list[Element] = [el19, el22, el19]
# # for el in elements:
# #     db.add(el)


# img1 = Image.fromarray(numpy.ones(shape=(2, 2, 3)).astype(numpy.uint8))
from PIL.PngImagePlugin import PngImageFile
img = Image.Image()
img1 = Image.open(Path(
    "/home/oem/Desktop/PhD/mySLAM/tests/data_manager/factory/batch_factory/api/test_data/image/stereo_left/19.png"))
bt = Image.frombytes(img1.tobytes())
img2 = Image.fromarray(numpy.ones(shape=(2, 2, 3)).astype(numpy.uint8))
# img2 = Image.open(Path(
#     "/home/oem/Downloads/urban18-highway/image/stereo_left/1544578498493167947.png"))
# and self.mode == other.mode
# and self.size == other.size
# and self.info == other.info
# and self.getpalette() == other.getpalette()
# and self.tobytes() == other.tobytes()
print(img1.__class__,  '\n', img2.__class__)
