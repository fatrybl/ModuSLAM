from csv import DictReader as dict_reader

from pathlib2 import Path

from data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.kaist.measurement_collector import MeasurementCollector
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import KaistDataset


class KaistReader(DataReader):
    def __init__(self):
        super().__init__()
        self.__sensor_order_file = self._dataset_dir / KaistDataset.data_stamp.value
        self.__collector = MeasurementCollector(self._dataset_dir)

    def __get_data_by_sensor(self, row):
        if row["sensor"] == "imu":
            self.__collector.get_imu()
        if row["sensor"] == "sick_back":
            self.__collector.get_lidar_2D()
        if row["sensor"] == "sick_middle":
            self.__collector.get_lidar_2D()
        if row["sensor"] == "velodyne_right":
            self.__collector.get_lidar_3D()
        if row["sensor"] == "velodyne_left":
            self.__collector.get_lidar_3D()
        if row["sensor"] == "fog":
            self.__collector.get_fog()
        if row["sensor"] == "encoder":
            self.__collector.get_encoder
        if row["sensor"] == "stereo":
            self.__collector.get_stereo()
        if row["sensor"] == "gps":
            self.__collector.get_gps()
        if row["sensor"] == "vrs":
            self.__collector.get_vrs()

    def get_element(self) -> Element:
        with open(self.__sensor_order_file, "r") as f:
            names = ["timestamp", "sensor"]
            reader = dict_reader(f, fieldnames=names)
            row = next(reader)
            self.__get_data_by_sensor(row)

        return self.__element
