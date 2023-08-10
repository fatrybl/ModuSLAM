from csv import DictReader as dict_reader
import logging

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import MeasurementCollector
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import KaistDataset
from slam.utils.stopping_criterion import StoppingCriterionSingleton

logger = logging.getLogger(__name__)


class KaistReader(DataReader):
    def __init__(self):
        super().__init__()
        self.__collector = MeasurementCollector(self._dataset_dir)
        self.__iterator = self.__init_iterator()
        self.__sensor_order_file = self._dataset_dir / KaistDataset.data_stamp.value
        self.__break_point = StoppingCriterionSingleton()

    def __init_iterator(self):
        if (DataReader.is_file_valid(self.__sensor_order_file)):
            with open(self.__sensor_order_file, "r") as f:
                names = ["timestamp", "sensor"]
                reader = dict_reader(f, fieldnames=names)
                for line in reader:
                    yield line
        else:
            logger.critical(
                f"Couldn't initialize the iterator for {self.__sensor_order_file}")
            self.__break_point.is_data_processed = True

    def __get_data_by_sensor(self, line):
        if line["sensor"] == "imu":
            message, location = self.__collector.get_imu()
        if line["sensor"] == "fog":
            message, location = self.__collector.get_fog()
        if line["sensor"] == "encoder":
            message, location = self.__collector.get_encoder()
        if line["sensor"] == "gps":
            message, location = self.__collector.get_gps()
        if line["sensor"] == "vrs":
            message, location = self.__collector.get_vrs_gps()
        if line["sensor"] == "altimeter":
            message, location = self.__collector.get_altimeter()
        if line["sensor"] == "sick_back":
            message, location = self.__collector.get_lidar_2D(line)
        if line["sensor"] == "sick_middle":
            message, location = self.__collector.get_lidar_2D(line)
        if line["sensor"] == "velodyne_right":
            message, location = self.__collector.get_lidar_3D(line)
        if line["sensor"] == "velodyne_left":
            message, location = self.__collector.get_lidar_3D(line)
        if line["sensor"] == "stereo":
            message, location = self.__collector.get_stereo(line)

        return message, location

    def get_element(self) -> Element:
        try:
            line = next(self.__iterator)
            message, location = self.__get_data_by_sensor(line)

            time = int(message["timestamp"])
            measurement = Measurement(line["sensor"], message["data"])

            return Element(time, measurement, location)

        except StopIteration:
            return None

        except Exception as e:
            logger.exception(e)

    def get_element_with_measurement(self, measurement: tuple) -> Element:
        raise NotImplementedError
