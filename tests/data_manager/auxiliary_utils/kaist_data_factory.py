import csv
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
from PIL import Image

from slam.data_manager.factory.readers.element_factory import Element
from slam.setup_manager.sensors_factory.sensors import Sensor


@dataclass
class SensorNamePath:
    name: str
    file_path: Path


@dataclass
class SensorElementPair:
    sensor: Sensor
    element: Element


class DataFactory:
    """
    Generates Kaist Urban-like Dataset with the given measurements.
    """

    def __init__(self, dataset_structure: Any) -> None:
        self.dataset_structure = dataset_structure

    @staticmethod
    def equal_images(el1: Element, el2: Element) -> bool:
        """
        Compares two elements with Image data.

        PIL images can not be compared directly because of different subclasses.
        Manualy created image from numpy.array is of type Image.Image,
        but the one obtained from file is of type PIL.PngImagePlugin.PngImageFile.

        Args:
            el1 (Element): 1-st element to be compared.
            el2 (Element): 2-nd element to be compared.

        Returns:
            bool: comparison result
        """
        el1_array_img1 = np.asarray(el1.measurement.values[0])
        el1_array_img2 = np.asarray(el1.measurement.values[1])
        el2_array_img1 = np.asarray(el2.measurement.values[0])
        el2_array_img2 = np.asarray(el2.measurement.values[1])
        result = np.array_equal(el1_array_img1, el2_array_img1) and np.array_equal(el1_array_img2, el2_array_img2)
        return result

    @staticmethod
    def flatten(data: Iterable[Any]) -> Iterator[Any]:
        """
        Flattens tuple of tuples for proper comparison,
        Args:
            data (Iterable[Any]): tuple of any-type-measurements

        Yields:
            Iterator[Any]: item in set.
        """
        for item in data:
            if isinstance(item, Iterable) and not isinstance(item, str):
                items = DataFactory.flatten(item)
                for x in items:
                    yield x
            else:
                yield item

    @staticmethod
    def to_binary_file(data: tuple[float, ...], path: Path) -> None:
        """
        Writes data to a binary file with floating point representation (float32)
        due to lidar measurements format in Kaist Urban Dataset.

        Args:
            data (tuple[float]): data to be written.
            path (Path): binary file path.
        """
        with open(path, "wb") as output_file:
            numpy_array = np.asarray(data, dtype=np.float32)
            numpy_array.tofile(output_file)

    @staticmethod
    def to_csv_file(
        data: Iterable[Any] | Iterable[Iterable[Any]],
        path: Path,
        multilines: bool = False,
    ) -> None:
        """
        Writes data to a CSV file.

        Args:
            data (Iterable[Iterable[int | str]] | Iterable[float | int]):
                data to be written to a CSV file.
            path (Path): file path.
            multilines (bool | None): If True: writes list[list[str]] to the file. Defaults to False.
        """
        with open(path, "a", encoding="UTF8", newline="") as outfile:
            writer = csv.writer(outfile)
            if multilines:
                writer.writerows(data)
            else:
                writer.writerow(data)

    @staticmethod
    def to_img_file(data: tuple[int, npt.NDArray[np.uint8]], path: Path) -> None:
        """
        Writes image to the given file path with OpenCV module.

        Args:
            data (tuple[int, npt.NDArray[np.float32]]): image as a numpy array.
            path (Path): file path.
        """
        img = Image.fromarray(data[1])
        img.save(path)

    def create_dataset_structure(self) -> None:
        """
        Creates Kaist Urban dataset empty directories & files structure.
        """
        for field in fields(self.dataset_structure):
            field_name: str = field.name
            field_value: Path | str = getattr(self.dataset_structure, field_name)

            if isinstance(field_value, Path):
                if field_value.suffix == "":
                    Path.mkdir(field_value, parents=True, exist_ok=True)
                else:
                    Path.touch(field_value)

    def generate_data(
        self,
        data_stamp: Iterable[list[int | str]],
        stamp_files: Iterable[tuple],
        csv_data: Iterable[tuple],
        binary_data: Iterable[tuple],
        image_data: Iterable[tuple],
    ) -> None:
        """
        Writes data to the directories & files.

        Args:
            data_stamp (list[list[int  |  str]]): content of data_stamp.csv
            stamp_files (Iterable[tuple]): content of <SENSOR>_stamp.csv
            csv_data (Iterable[tuple]): sensor data in csv format.
            binary_data (Iterable[tuple]): sensor data in binary format.
            image_data (Iterable[tuple]): sensor data in image-based format.
        """

        self.to_csv_file(data_stamp, self.dataset_structure.data_stamp, multilines=True)

        for element, path in stamp_files:
            self.to_csv_file(element, path)

        for element, path in csv_data:
            self.to_csv_file(element, path)

        for element, path in binary_data:
            self.to_binary_file(element, path)

        for element, path in image_data:
            self.to_img_file(element, path)
