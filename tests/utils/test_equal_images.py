"""Tests for the equal_images method in the auxiliary_methods module."""

import numpy as np
from PIL import Image

from moduslam.utils.auxiliary_methods import equal_images


def test_equal_images():
    # Create two identical images
    data = np.uint8(np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]]))
    img1 = Image.fromarray(data)
    img2 = Image.fromarray(data)

    # Use the equal_images method to compare the images
    assert equal_images((img1,), (img2,)) is True

    # Create two different images
    data_diff = np.uint8(np.array([[255, 255, 255], [0, 0, 0], [255, 255, 255]]))
    img3 = Image.fromarray(data_diff)

    # Use the equal_images method to compare the different images
    assert equal_images((img1,), (img3,)) is False
