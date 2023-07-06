from csv import DictReader as dict_reader
from pathlib2 import Path

from data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.kaist.measurement_collector import MeasurementCollector
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import KaistDataset


class KaistReader(DataReader):
    def __init__(self):
        super().__init__()
        self.__collector = MeasurementCollector(self._dataset_dir)
        self.__iterator = self.__init_iterator()
        self.__element = Element
        self.__sensor_order_file = self._dataset_dir / KaistDataset.data_stamp.value

    @property
    def element(self):
        if self.__element:
            return self.__element
        else:
            raise ValueError("No element")

    def __init_iterator(self):
        with open(self.__sensor_order_file, "r") as f:
            names = ["timestamp", "sensor"]
            reader = dict_reader(f, fieldnames=names)
            for line in reader:
                yield line

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

    def get_element(self):
        try:
            line = next(self.__iterator)
            message, location = self.__get_data_by_sensor(line)
            time = int(message["timestamp"])
            measurement = {"sesnsor": line["sensor"]}
            measurement.update(data=message["data"])
            self.__element = Element(time, measurement, location)

        except StopIteration:
            # log exception
            self.__element = None

    def get_element_with_measurement(self, measurement: tuple) -> Element:
        raise NotImplementedError
