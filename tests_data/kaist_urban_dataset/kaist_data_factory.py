import csv
from dataclasses import fields
from pathlib import Path
from typing import Any, overload

import numpy as np
from PIL import Image
from plum import dispatch

from tests_data.kaist_urban_dataset.data import (
    binary_data,
    csv_data,
    data_stamp,
    image_data,
    stamp_files,
)
from tests_data.kaist_urban_dataset.structure import DatasetStructure


class DataFactory:
    """Generates Kaist Urban-like Dataset with the given measurements."""

    def __init__(self, structure: DatasetStructure) -> None:
        self.dataset_structure = structure

    @staticmethod
    def to_binary_file(data: tuple[float, ...], path: Path) -> None:
        """Writes data to a binary file with floating point representation (float32) due
        to lidar measurements format in Kaist Urban Dataset.

        Args:
            data (tuple[float]): data to be written.
            path (Path): binary file path.
        """
        with open(path, "wb") as output_file:
            numpy_array = np.asarray(data, dtype=np.float32)
            numpy_array.tofile(output_file)

    @staticmethod
    @overload
    def to_csv_file(data: int, path: Path) -> None:
        """Writes new row to a CSV file.

        Args:
            data (int): number to be written to a CSV file.
            path (Path): file path.
        """
        with open(path, "a", encoding="UTF8", newline="") as outfile:
            writer = csv.writer(outfile)
            row = [str(data)]
            writer.writerow(row)

    @staticmethod
    @overload
    def to_csv_file(data: tuple[int | float, ...], path: Path) -> None:
        """Writes new row to a CSV file.

        Args:
            data (tuple[float | int, ...]): data to be written to a CSV file.
            path (Path): file path.
        """
        with open(path, "a", encoding="UTF8", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)

    @staticmethod
    @overload
    def to_csv_file(data: list[list[int | str]], path: Path) -> None:
        """Writes multiple rows to a CSV file.

        Args:
            data (list[list[int | str]]): data to be written to a CSV file.
            path (Path): file path.
        """
        with open(path, "a", encoding="UTF8", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerows(data)

    @staticmethod
    @dispatch
    def to_csv_file(self, path=None): ...

    @staticmethod
    def to_img_file(data: tuple[int, np.ndarray[Any, np.dtype]], path: Path) -> None:
        """Writes image to the given file path with OpenCV module.

        Args:
            data (tuple[int, npt.NDArray[np.float32]]): image as a numpy array.
            path (Path): file path.
        """
        img = Image.fromarray(data[1])
        img.save(path)

    def create_dataset_structure(self) -> None:
        """Creates Kaist Urban dataset empty directories & files structure."""
        for field in fields(self.dataset_structure):
            field_name: str = field.name
            field_value: Path | str = getattr(self.dataset_structure, field_name)

            if isinstance(field_value, Path):
                if field_value.suffix == "":
                    Path.mkdir(field_value, parents=True, exist_ok=True)
                else:
                    Path.touch(field_value)

    def generate_csv(self):
        for elements, path in csv_data:
            self.to_csv_file(elements, path)

    def generate_stamp_files(self):
        self.to_csv_file(data_stamp, self.dataset_structure.data_stamp_file)

        for elements, path in stamp_files:
            self.to_csv_file(elements, path)

    def generate_img(self):
        for elements, path in image_data:
            self.to_img_file(elements, path)

    def generate_binary(self):
        for elements, path in binary_data:
            self.to_binary_file(elements, path)

    def generate_data(self) -> None:
        """Writes data to the directories & files."""
        self.create_dataset_structure()

        self.generate_stamp_files()
        self.generate_csv()
        self.generate_img()
        self.generate_binary()
